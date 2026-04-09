from itertools import count
from typing import Iterator
from eliot.DAG import DAGNode, DecisionNode, ActionNode, DAG
from .types import Case

def build_cases(
    node: DAGNode, 
    counter: Iterator[int], 
    path: list[str]
) -> Case:
    """
    Recursively transform a DAGNode into a Case-based
    intermediate representation.

    A unique numeric identifier is assigned to every case,
    ensuring deterministic switch-based code generation.

    Args:
        node: DAG node to process
        counter: Counter used for generating unique case identifiers
        path: Path to node id DAG

    Returns:
        Prepared case node
    """

    # Generate unique identifier for this case
    node_id = next(counter)

    if isinstance(node, DecisionNode):
        return {
            "id": node_id,
            "type": "DecisionCase",
            "condition": node.condition,

            # Recursively build true/false branches
            "if_true": build_cases(
                node.if_true, 
                counter, 
                path + [f"DECISION({node.condition.conditionType})=true"]
            ),
            "if_false": build_cases(
                node.if_false, 
                counter, 
                path + [f"DECISION({node.condition.conditionType})=false"]
            ),

            # Metadata for comment generation
            "path": path,
            "label": f"DECISION({node.condition.conditionType})"
        }
    elif isinstance(node, ActionNode):
        return {
            "id": node_id,
            "type": "ActionCase",
            "action": node.action,
            "final": node.action.is_final,
            # Recursively process continuation if exists
            "next": build_cases(
                node.next, 
                counter, 
                path + [f"ACTION({node.action.actionType})"]
            ) if node.next else None,

            # Metadata for comment generation
            "path": path,
            "label": f"ACTION({node.action.actionType})"
        }
    else:
        return {
            "id": node_id,
            "type": "StateCase",
            "state_node": node,
            # Each transition is converted into a Case
            "transitions": [
                (
                    transition.state, build_cases(
                        transition.next, 
                        counter, 
                        path + [f"STATE({node.id})={transition.state}"]
                    )
                )
                for transition in node.transitions
            ],
            
            # Metadata for comment generation
            "path": path,
            "label": f"STATE({node.id})"
        }

def flatten_cases(root: Case) -> list[Case]:
    """
    Flatten Case tree into a linear list.
    
    Args:
        root: Extracted Root case from DAG
    
    Returns:
        List of Cases
    """

    result: list[Case] = []

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

def get_cases(dag: DAG) -> list[Case]:
    """
    Convert DAG into flattened Case list.
    """

    # Uses iterator to guarantee unique node ids
    root = build_cases(dag.root, count(0), ["ROOT"])
    return flatten_cases(root)
