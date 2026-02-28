from typing import Set, Tuple
from src.DAG import Condition, Action, ValueGeneratorBase, StateNode, DecisionNode, ActionNode, DAGNode

def get_generators(
    node: Condition | Action
) -> Set[ValueGeneratorBase[str, float | int]]:
    """
    Extract value generators from a Condition or Action instance.

    The function inspects the internal attributes of the node and
    collects all ValueGeneratorBase instances used for runtime value
    generation.

    Args:
        node: DAG node to extract generators from
    
    Returns:
        Set of collected value generators.
    """

    return {
        v
        for v in node.__dict__.values() 
        if isinstance(v, ValueGeneratorBase)
    }

def collect_nodes(
    node: DAGNode
) -> Tuple[
    Set[Condition],
    Set[Action],
    Set[StateNode],
    Set[ValueGeneratorBase[str, float | int]]
]:
    """
    Recursively traverse the DAG and collect all unique nodes.

    Args:
        node: DAG node to process.

    Returns:
        Set of recursively collected nodes.
    """

    conditions: Set[Condition] = set()
    actions: Set[Action] = set()
    states: Set[StateNode] = set()
    generators: Set[ValueGeneratorBase[str, float | int]] = set()

    if isinstance(node, DecisionNode):
        # Collect condition from decision node
        conditions.add(node.condition)
        generators |= get_generators(node.condition)

        # Recursively process both branches
        conditions_true, actions_true, states_true, generators_true = collect_nodes(node.if_true)
        conditions_false, actions_false, states_false, generators_false = collect_nodes(node.if_false)

        # Merge results
        conditions |= conditions_true | conditions_false
        actions |= actions_true | actions_false
        states |= states_true | states_false
        generators |= generators_true | generators_false

    elif isinstance(node, ActionNode):
        # Collect action
        actions.add(node.action)
        generators |= get_generators(node.action)

        # Continue traversal if action has continuation
        if node.next is not None:
            conditions_next, actions_next, states_next, generators_next = collect_nodes(node.next)

            # Merge results
            conditions |= conditions_next
            actions |= actions_next
            states |= states_next
            generators |= generators_next

    else:
        states.add(node)

        # Recursively traverse state transitions
        for t in node.transitions:
            conditions_transition, actions_transition, states_transition, generators_transition = collect_nodes(t.next)

            # Merge results
            conditions |= conditions_transition
            actions |= actions_transition
            states |= states_transition
            generators |= generators_transition

    return conditions, actions, states, generators
