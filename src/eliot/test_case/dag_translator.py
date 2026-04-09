from typing import cast
from eliot.DAG.dag import DAG, ActionNode, DecisionNode
from eliot.DAG.actions import Action
from eliot.DAG.actions.drop import Drop
from eliot.DAG.actions.finish import Finish
from .test_case import TestCase, Rule

def build_action_chain(
    actions: list[Action],
    default_node: ActionNode | DecisionNode
) -> ActionNode:
    """
    Construct a sequential chain of ActionNode objects.

    Actions are linked in reverse order so that the first
    action in the list becomes the first executed node.

    Args:
        actions: List of actions
        default_node: Node which is attached to first action

    Return:
        Action node with chained action nodes
    """

    if not actions:
        raise ValueError("Rule must contain at least one action")

    # Default node is at the end of action chain
    next_node: ActionNode | DecisionNode = default_node

    # Iterates in reversed to build list from bottom
    for action in reversed(actions):
        next_node = ActionNode(
            action=action, 
            next=None if action.is_final else next_node        # Final actions dont have next
        )

    # Build chain bottom-up
    return cast(ActionNode, next_node)

def build_rule_tree(
    rule: Rule,
    default_node: ActionNode | DecisionNode
) -> ActionNode | DecisionNode:
    """
    Convert a single Rule into a DecisionNode tree.

    Args:
        rule: Rule to convert
        default_node: Default node to use as List node

    Returns:
        Built tree
    """

    actions_chain = build_action_chain(rule.actions, default_node)

    # Reverse conditions to create tree from bottom
    conditions = list(reversed(rule.conditions))

    # Action chain follows after last condition
    next_node: ActionNode | DecisionNode = actions_chain

    for i, condition in enumerate(conditions):
        if rule.type == "all":
            # All decision nodes have to be true to execute action chain
            next_node = DecisionNode(
                condition=condition, 
                if_true=next_node, 
                if_false=default_node
            )
        else:
            # At least one satisfied decision node is required to execute action chain
            next_node = DecisionNode(
                condition=condition, 
                if_true=actions_chain, 
                if_false=next_node if i > 0 else default_node
            )

    return next_node

def translate_to_DAG(test_case: TestCase) -> DAG:
    """
    Translate TestCase into a DAG structure.

    Args:
        test_case: TestCase to translate.
    
    Returns:
        Translated DAG object.
    """

    # Creates default action based on value from test case
    default_action = (
        Drop(actionType="Drop") 
        if test_case.defaultAction == "Drop" 
        else Finish(actionType="Finish")
    )

    # Creates default ActionNode to add to the bottom of the tree
    default_node = ActionNode(action=default_action, next=None)

    # No rules given default action is applied to all packets
    if not test_case.rules:
        return DAG(root=default_node)

    # Save next node
    next_default: DecisionNode | ActionNode = default_node

    # Iterate over all rules in reverse order to build tree from bottom
    for rule in reversed(test_case.rules):
        next_default = build_rule_tree(rule, next_default)

    return DAG(root=next_default)
