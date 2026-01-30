from __future__ import annotations
from itertools import count
from src.DAG.actions.change_state import ChangeState
from src.DAG.generators import ValueGeneratorBase
from src.DAG.actions import Action
from src.DAG.guards import Guard
from src.DAG import DAGNode, StateNode, DAG, GuardNode, ActionNode
from typing import Dict, Tuple, Set, TypedDict, Literal, Optional, Iterator, List

def get_generators(node: Guard | Action) -> Set[ValueGeneratorBase[str, float | int]]:
    """Iterates over node instance internal dictionary values and collect all generators"""
    return { v for v in node.__dict__.values() if isinstance(v, ValueGeneratorBase) }

def collect_nodes(node: DAGNode) -> Tuple[Set[Guard], Set[Action], Set[StateNode], Set[ValueGeneratorBase[str, float | int]]]:
    """Collect Guards, Actions and generators from DAG starting from root node"""

    guards: Set[Guard] = set()
    actions: Set[Action] = set()
    states: Set[StateNode] = set()
    generators: Set[ValueGeneratorBase[str, float | int]] = set()

    if isinstance(node, GuardNode):
        guards.add(node.guard)
        generators |= get_generators(node.guard)

        # Collect nodes from subtrees
        guards_true, actions_true, states_true, generators_true = collect_nodes(node.if_true)
        guards_false, actions_false, states_false, generators_false = collect_nodes(node.if_false)

        # Join results
        guards |= guards_true | guards_false
        actions |= actions_true | actions_false
        states |= states_true | states_false
        generators |= generators_true | generators_false

    elif isinstance(node, ActionNode):
        actions.add(node.action)
        generators |= get_generators(node.action)
        if node.next is not None:
            # Collect nodes from subtree
            guards_next, actions_next, states_next, generators_next = collect_nodes(node.next)

            # Join results
            guards |= guards_next
            actions |= actions_next
            states |= states_next
            generators |= generators_next

    else:
        states.add(node)
        # Collect nodes from subtrees
        for t in node.transitions:
            guards_transition, actions_transition, states_transition, generators_transition = collect_nodes(t.next)

            # Join results
            guards |= guards_transition
            actions |= actions_transition
            states |= states_transition
            generators |= generators_transition

    return guards, actions, states, generators

class GuardCase(TypedDict):
    """Class representing Guard context for generating"""
    id: int
    type: Literal["GuardCase"]
    guard: Guard
    if_true: Case
    if_false: Case

class ActionCase(TypedDict):
    """Class representing Action context for generating"""
    id: int
    type: Literal["ActionCase"]
    action: Action
    final: bool
    next: Optional[Case]

class StateCase(TypedDict):
    """Class representing State context for generating"""
    id: int
    type: Literal["StateCase"]
    state_node: StateNode
    transitions: List[Tuple[str, Case]]

Case = GuardCase | ActionCase | StateCase

def build_cases(node: DAGNode, counter: Iterator[int]) -> Case:
    """Traverse DAG and convert nodes to `Case`"""

    # Determine unique node id used in switch
    node_id = next(counter)

    if isinstance(node, GuardNode):
        return {
            "id": node_id,
            "type": "GuardCase",
            "guard": node.guard,

            # Process subtree nodes
            "if_true": build_cases(node.if_true, counter),
            "if_false": build_cases(node.if_false, counter),
        }
    elif isinstance(node, ActionNode):
        return {
            "id": node_id,
            "type": "ActionCase",
            "action": node.action,
            "final": node.final,
            # Process subtree node if present
            "next": build_cases(node.next, counter) if node.next else None
        }
    else:
        return {
            "id": node_id,
            "type": "StateCase",
            "state_node": node,
            "transitions": [(transition.state, build_cases(transition.next, counter)) for transition in node.transitions]
        }

def flatten_cases(root: Case) -> List[Case]:
    """Creates list of cases from case tree"""

    result: List[Case] = []

    # Recursive inorder traversing flattening function
    def flatten(node: Case) -> None:
        result.append(node)
        if node["type"] == "GuardCase":
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
    root = build_cases(dag.root, count(0))
    return flatten_cases(root)

def process_state_nodes(state_nodes: Set[StateNode], action_nodes: List[ChangeState], cases: List[Case]) -> None:
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
    for action in action_nodes:
        if action.target not in state_node_map:
            raise ValueError(f"Undefined reference to state node in ChangeState action: {action.target}")

        target_node = state_node_map[action.target]
        if action.state not in target_node.states():
            raise ValueError(f"Cannot set undefined state {action.state} to StateNode with id: {target_node.id}")

        # Attach `StateNode` to action node for generating
        action.attach_state_node_type(target_node.cpp_type())
