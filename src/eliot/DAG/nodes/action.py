from __future__ import annotations
from pydantic import model_validator
from eliot.DAG.actions import Action
from .node import DAGNode

class ActionNode(DAGNode):
    """
    Represents an executable action node in the DAG.

    ActionNode encapsulates a concrete Action instance and optionally
    references the next node in the execution chain.
    """

    # Action to be executed
    action: Action

    # Continuation node (None only if action is final)
    next: DAGNode | None = None

    @model_validator(mode="after")
    def check_next_vs_final(self) -> ActionNode:
        """
        Enforce structural invariant:

        - Final actions must NOT have a next node.
        - Non-final actions MUST have a next node.
        """
        if self.action.is_final and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.action.is_final and self.next is None:
            raise ValueError("Non final action node requires next node")
        return self
