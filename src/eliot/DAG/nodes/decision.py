from eliot.DAG.conditions import Condition
from .node import DAGNode

class DecisionNode(DAGNode):
    """
    Represents a conditional branching node in the DAG.

    A DecisionNode evaluates a Condition and selects one of two branches.
    """

    # Condition to evaluate
    condition: Condition

    # Branch taken if condition evaluates to true
    if_true: DAGNode

    # Branch taken if condition evaluates to false
    if_false: DAGNode
