from typing import List, cast
from ..DAG.dag import DAG, ActionNode, GuardNode
from .test_case import TestCase, Rule
from ..DAG.actions import Action, Drop, Finish

def build_action_chain(actions: List[Action], default_node: ActionNode | GuardNode) -> ActionNode:
    if not actions:
        raise ValueError("Rule must contain at least one action")

    next_node: ActionNode | GuardNode = default_node
    for i, action in enumerate(reversed(actions)):
        is_last = i == 0
        next_node = ActionNode(action=action, final=is_last and action.actionType in ["Finish", "Drop"], next=None if is_last and action.actionType in ["Finish", "Drop"] else next_node)
    return cast(ActionNode, next_node)

def build_rule_tree(rule: Rule, default_node: ActionNode | GuardNode) -> GuardNode | ActionNode:
    actions_chain = build_action_chain(rule.actions, default_node)
    guards = list(reversed(rule.guards))

    next_node: GuardNode | ActionNode = actions_chain

    for i, guard in enumerate(guards):
        if rule.type == "all":
            next_node = GuardNode(guard=guard, if_true=next_node, if_false=default_node)
        else:
            next_node = GuardNode(guard=guard, if_true=actions_chain, if_false=next_node if i > 0 else default_node)
    return next_node

def translate_to_DAG(test_case: TestCase) -> DAG:
    default_action = Drop(actionType="Drop") if test_case.defaultAction == "Drop" else Finish(actionType="Finish")
    default_node = ActionNode(final=True, action=default_action, next=None)

    if not test_case.rules:
        return DAG(root=default_node)

    next_default: GuardNode | ActionNode = default_node

    for rule in reversed(test_case.rules):
        next_default = build_rule_tree(rule, next_default)

    return DAG(root=next_default)
