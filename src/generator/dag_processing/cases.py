from itertools import count
from typing import Iterator, List
from src.DAG import DAGNode, DecisionNode, ActionNode, DAG
from .types import Case

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
            "final": node.action.is_final(),
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
