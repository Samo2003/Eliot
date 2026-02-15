from typing import List, cast
from ..DAG.dag import DAG, ActionNode, DecisionNode
from .test_case import TestCase, Rule
from ..DAG.actions import Action, Drop, Finish

def build_action_chain(actions: List[Action], default_node: ActionNode | DecisionNode) -> ActionNode:
    """Creates a list of Action nodes in DAG"""

    if not actions:
        raise ValueError("Rule must contain at least one action")

    # Default node is at the end of action chain
    next_node: ActionNode | DecisionNode = default_node

    # Iterates in reversed to build list from bottom
    for i, action in enumerate(reversed(actions)):
        # First action is final if it is one of final action nodes
        final = i == 0 and action.actionType in ["Finish", "Drop"]

        next_node = ActionNode(
            action=action, 
            final=final,
            next=None if final else next_node           # Final actions dont have next
        )

    # Cast only to satisfy Pylance because rule must contain at least one action 
    # so next node is always action node
    return cast(ActionNode, next_node)

def build_rule_tree(rule: Rule, default_node: ActionNode | DecisionNode) -> DecisionNode | ActionNode:
    """Builds tree from given rule"""

    actions_chain = build_action_chain(rule.actions, default_node)

    # Reverse conditions to create tree from bottom
    conditions = list(reversed(rule.conditions))

    # Action chain follows after last condition
    next_node: DecisionNode | ActionNode = actions_chain

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
    """Translates test case to DAG"""

    # Creates default action based on value from test case
    default_action = Drop(actionType="Drop") if test_case.defaultAction == "Drop" else Finish(actionType="Finish")

    # Creates default ActionNode to add to the bottom of the tree
    default_node = ActionNode(final=True, action=default_action, next=None)

    # No rules given default action is applied to all packets
    if not test_case.rules:
        return DAG(root=default_node)

    # Save next node
    next_default: DecisionNode | ActionNode = default_node

    # Iterate over all rules in reverse order to build tree from bottom
    for rule in reversed(test_case.rules):
        next_default = build_rule_tree(rule, next_default)

    return DAG(root=next_default)
