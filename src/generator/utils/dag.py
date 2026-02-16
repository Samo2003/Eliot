from __future__ import annotations
from itertools import count
from src.DAG.actions.change_state import ChangeState
from src.DAG.generators import ValueGeneratorBase
from src.DAG.actions import Action
from src.DAG.conditions import Condition
from src.DAG import DAGNode, StateNode, DAG, DecisionNode, ActionNode
from typing import Dict, Tuple, Set, TypedDict, Literal, Optional, Iterator, List

def get_generators(node: Condition | Action) -> Set[ValueGeneratorBase[str, float | int]]:
    """Iterates over node instance internal dictionary values and collect all generators"""
    return { v for v in node.__dict__.values() if isinstance(v, ValueGeneratorBase) }

def collect_nodes(node: DAGNode) -> Tuple[Set[Condition], Set[Action], Set[StateNode], Set[ValueGeneratorBase[str, float | int]]]:
    """Collect Conditions, Actions and generators from DAG starting from root node"""

    conditions: Set[Condition] = set()
    actions: Set[Action] = set()
    states: Set[StateNode] = set()
    generators: Set[ValueGeneratorBase[str, float | int]] = set()

    if isinstance(node, DecisionNode):
        conditions.add(node.condition)
        generators |= get_generators(node.condition)

        # Collect nodes from subtrees
        conditions_true, actions_true, states_true, generators_true = collect_nodes(node.if_true)
        conditions_false, actions_false, states_false, generators_false = collect_nodes(node.if_false)

        # Join results
        conditions |= conditions_true | conditions_false
        actions |= actions_true | actions_false
        states |= states_true | states_false
        generators |= generators_true | generators_false

    elif isinstance(node, ActionNode):
        actions.add(node.action)
        generators |= get_generators(node.action)
        if node.next is not None:
            # Collect nodes from subtree
            conditions_next, actions_next, states_next, generators_next = collect_nodes(node.next)

            # Join results
            conditions |= conditions_next
            actions |= actions_next
            states |= states_next
            generators |= generators_next

    else:
        states.add(node)
        # Collect nodes from subtrees
        for t in node.transitions:
            conditions_transition, actions_transition, states_transition, generators_transition = collect_nodes(t.next)

            # Join results
            conditions |= conditions_transition
            actions |= actions_transition
            states |= states_transition
            generators |= generators_transition

    return conditions, actions, states, generators


class DecisionCase(TypedDict):
    """Class representing Decision context for generating"""

    id: int
    type: Literal["DecisionCase"]
    condition: Condition
    if_true: Case
    if_false: Case
    path: List[str]
    label: str

class ActionCase(TypedDict):
    """Class representing Action context for generating"""

    id: int
    type: Literal["ActionCase"]
    action: Action
    final: bool
    next: Optional[Case]
    path: List[str]
    label: str

class StateCase(TypedDict):
    """Class representing State context for generating"""

    id: int
    type: Literal["StateCase"]
    state_node: StateNode
    transitions: List[Tuple[str, Case]]
    path: List[str]
    label: str

Case = DecisionCase | ActionCase | StateCase

def build_cases(node: DAGNode, counter: Iterator[int], path: List[str]) -> Case:
    """Traverse DAG and convert nodes to `Case`"""

    # Determine unique node id used in switch
    node_id = next(counter)

    if isinstance(node, DecisionNode):
        return {
            "id": node_id,
            "type": "DecisionCase",
            "condition": node.condition,

            # Process subtree nodes
            "if_true": build_cases(node.if_true, counter, path + [f"DECISION({node.condition.conditionType})=true"]),
            "if_false": build_cases(node.if_false, counter, path + [f"DECISION({node.condition.conditionType})=false"]),
            "path": path,
            "label": f"DECISION({node.condition.conditionType})"
        }
    elif isinstance(node, ActionNode):
        return {
            "id": node_id,
            "type": "ActionCase",
            "action": node.action,
            "final": node.final,
            # Process subtree node if present
            "next": build_cases(node.next, counter, path + [f"ACTION({node.action.actionType})"]) if node.next else None,
            "path": path,
            "label": f"ACTION({node.action.actionType})"
        }
    else:
        return {
            "id": node_id,
            "type": "StateCase",
            "state_node": node,
            "transitions": [(transition.state, build_cases(transition.next, counter, path + [f"STATE({node.id})={transition.state}"])) for transition in node.transitions],
            "path": path,
            "label": f"STATE({node.id})"
        }

def flatten_cases(root: Case) -> List[Case]:
    """Creates list of cases from case tree"""

    result: List[Case] = []

    # Recursive inorder traversing flattening function
    def flatten(node: Case) -> None:
        result.append(node)
        if node["type"] == "DecisionCase":
            flatten(node["if_true"])
            flatten(node["if_false"])
        elif node["type"] == "StateCase":
            for _, n in node["transitions"]:
                flatten(n)
        elif node["next"] is not None:
            flatten(node["next"])

    flatten(root)
    return result

def get_cases(dag: DAG) -> List[Case]:
    """Creates case list context from DAG"""

    # Uses iterator to guarantee unique node ids
    root = build_cases(dag.root, count(0), ["ROOT"])
    return flatten_cases(root)

def process_state_nodes(state_nodes: Set[StateNode], actions: List[ChangeState], cases: List[Case]) -> None:
    def find_case(id: str) -> StateCase:
        for case in cases:
            if case["type"] != "StateCase":
                continue
            if case["state_node"].id == id:
                return case
        raise RuntimeError(f"StateCase not found for StateNode with id: {id}")

    # Build ID to `StateNode` map and attach transition IDs
    state_node_map: Dict[str, StateNode] = {}
    for node in state_nodes:
        if node.id in state_node_map:
            raise ValueError(f"Duplicate StateNode id detected: {node.id}")
        state_node_map[node.id] = node

        # Attach transition IDs to `StateNode`
        node.attach_transition_ids(find_case(node.id))
    
    # Verify action references to StateNodes
    for action in actions:
        if action.target not in state_node_map:
            raise ValueError(f"Undefined reference to state node in ChangeState action: {action.target}")

        target_node = state_node_map[action.target]
        if action.state not in target_node.states():
            raise ValueError(f"Cannot set undefined state {action.state} to StateNode with id: {target_node.id}")

        # Attach `StateNode` to action node for generating
        action.attach_state_node_type(target_node.cpp_type())
