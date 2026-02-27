from typing import Set, Tuple
from src.DAG import Condition, Action, ValueGeneratorBase, StateNode, DecisionNode, ActionNode, DAGNode

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
