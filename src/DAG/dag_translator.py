from typing import List, cast
from dag import DAG, ActionNode, GuardNode
from test_case import TestCase, Rule
from action import Action, Drop, Finish

def build_action_chain(actions: List[Action], default_node: ActionNode | GuardNode) -> ActionNode:
    if not actions:
        raise ValueError("Rule must contain at least one action")

    next_node: ActionNode | GuardNode = default_node
    for i, action in enumerate(reversed(actions)):
        is_last = i == 0
        next_node = ActionNode(type="action", action=action, final=is_last and action.actionType in ["Finish", "Drop"], next=None if is_last and action.actionType in ["Finish", "Drop"] else next_node)
    return cast(ActionNode, next_node)

def build_rule_tree(rule: Rule, default_node: ActionNode | GuardNode) -> GuardNode | ActionNode:
    actions_chain = build_action_chain(rule.actions, default_node)
    guards = list(reversed(rule.guards))

    next_node: GuardNode | ActionNode = actions_chain

    for i, guard in enumerate(guards):
        if rule.type == "all":
            next_node = GuardNode(type="guard", guard=guard, if_true=next_node, if_false=default_node)
        else:
            next_node = GuardNode(type="guard", guard=guard, if_true=actions_chain, if_false=next_node if i > 0 else default_node)
    return next_node

def translate_to_DAG(test_case: TestCase) -> DAG:
    default_action = Drop(actionType="Drop") if test_case.defaultAction == "drop" else Finish(actionType="Finish")
    default_node = ActionNode(type="action", final=True, action=default_action, next=None)

    if not test_case.rules:
        return DAG(root=default_node)

    next_default: GuardNode | ActionNode = default_node

    for rule in reversed(test_case.rules):
        next_default = build_rule_tree(rule, next_default)

    return DAG(root=next_default)


# Test
import json

with open("test.json", "r") as file:
    data = json.load(file)

test_case = TestCase.model_validate(data)
print(json.dumps(test_case.model_dump(), indent=4))

dag = translate_to_DAG(test_case)
print(json.dumps(dag.model_dump(), indent=4))
