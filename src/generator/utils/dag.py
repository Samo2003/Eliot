from __future__ import annotations
from itertools import count
from src.DAG.generators import ValueGeneratorBase
from ...DAG import *
from typing import Tuple, Set, TypedDict, Literal, Optional, Iterator, List

def get_generators(node: Guard | Action) -> Set[ValueGeneratorBase[str, float | int]]:
    return { v for v in node.__dict__.values() if isinstance(v, ValueGeneratorBase) }

def collect_nodes(node: GuardNode | ActionNode) -> Tuple[Set[Guard], Set[Action], Set[ValueGeneratorBase[str, float | int]]]:
    guards: Set[Guard] = set()
    actions: Set[Action] = set()
    generators: Set[ValueGeneratorBase[str, float | int]] = set()

    if isinstance(node, GuardNode):
        guards.add(node.guard)
        generators |= get_generators(node.guard)
        guards_true, actions_true, generators_true = collect_nodes(node.if_true)
        guards_false, actions_false, generators_false = collect_nodes(node.if_false)
        guards |= guards_true | guards_false
        actions |= actions_true | actions_false
        generators |= generators_true | generators_false

    else:
        actions.add(node.action)
        if node.next is not None:
            guards_next, actions_next, generators_next = collect_nodes(node.next)
            guards |= guards_next
            actions |= actions_next
            generators |= generators_next

    return guards, actions, generators

class GuardCase(TypedDict):
    id: int
    type: Literal["GuardCase"]
    guard: Guard
    if_true: Case
    if_false: Case

class ActionCase(TypedDict):
    id: int
    type: Literal["ActionCase"]
    action: Action
    final: bool
    next: Optional[Case]

Case = GuardCase | ActionCase

def build_cases(node: GuardNode | ActionNode, counter: Iterator[int]) -> Case:
    node_id = next(counter)

    if isinstance(node, GuardNode):
        return {
            "id": node_id,
            "type": "GuardCase",
            "guard": node.guard,
            "if_true": build_cases(node.if_true, counter),
            "if_false": build_cases(node.if_false, counter),
        }
    else:
        return {
            "id": node_id,
            "type": "ActionCase",
            "action": node.action,
            "final": node.final,
            "next": build_cases(node.next, counter) if node.next else None
        }

def flatten_cases(root: Case) -> List[Case]:
    result: List[Case] = []

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
    root = build_cases(dag.root, count(0))
    return flatten_cases(root)
