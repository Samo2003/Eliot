from __future__ import annotations
from itertools import count
from src.DAG.generators import ValueGeneratorBase
from ...DAG import *
from typing import Tuple, Set, TypedDict, Literal, Optional, Iterator, List

def get_generators(node: Guard | Action) -> Set[ValueGeneratorBase[str, float | int]]:
    """Iterates over node instance internal dictionary values and collect all generators"""
    return { v for v in node.__dict__.values() if isinstance(v, ValueGeneratorBase) }

def collect_nodes(node: GuardNode | ActionNode) -> Tuple[Set[Guard], Set[Action], Set[ValueGeneratorBase[str, float | int]]]:
    """Collect Guards, Actions and generators from DAG starting from root node"""

    guards: Set[Guard] = set()
    actions: Set[Action] = set()
    generators: Set[ValueGeneratorBase[str, float | int]] = set()

    if isinstance(node, GuardNode):
        guards.add(node.guard)
        generators |= get_generators(node.guard)

        # Collect nodes from subtrees
        guards_true, actions_true, generators_true = collect_nodes(node.if_true)
        guards_false, actions_false, generators_false = collect_nodes(node.if_false)

        # Join results
        guards |= guards_true | guards_false
        actions |= actions_true | actions_false
        generators |= generators_true | generators_false

    else:
        actions.add(node.action)
        generators |= get_generators(node.action)
        if node.next is not None:
            # Collect nodes from subtree
            guards_next, actions_next, generators_next = collect_nodes(node.next)

            # Join results
            guards |= guards_next
            actions |= actions_next
            generators |= generators_next

    return guards, actions, generators

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

Case = GuardCase | ActionCase

def build_cases(node: GuardNode | ActionNode, counter: Iterator[int]) -> Case:
    """Traverse DAG and convert nodes to `GuardCase` or `ActionCase`"""

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
    else:
        return {
            "id": node_id,
            "type": "ActionCase",
            "action": node.action,
            "final": node.final,
            # Process subtree node if present
            "next": build_cases(node.next, counter) if node.next else None
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
        elif node["next"] is not None:
            flatten(node["next"])

    flatten(root)
    return result

def get_cases(dag: DAG) -> List[Case]:
    """Creates case list context from DAG"""

    # Uses iterator to guarantee unique node ids
    root = build_cases(dag.root, count(0))
    return flatten_cases(root)
