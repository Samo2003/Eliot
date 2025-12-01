from __future__ import annotations
from pydantic import BaseModel, model_validator
from .guards import Guard
from .actions import Action

class ActionNode(BaseModel):
    """Represents an Action node in DAG"""

    # Indicates if action is final
    final: bool = False

    # Contains action to perform
    action: Action

    next: GuardNode | ActionNode | None = None

    @model_validator(mode="after")
    def check_next_vs_final(self):
        """Final node cannot have next and non final node must have next"""
        if self.final and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.final and self.next is None:
            raise ValueError("Non final action node requires next node")
        return self

class GuardNode(BaseModel):
    """Represents a Guard node in DAG"""

    # Contains guard to check
    guard: Guard

    if_true: GuardNode | ActionNode
    if_false: GuardNode | ActionNode


class DAG(BaseModel):
    """DAG root container containing Action node or Guard node"""
    root: GuardNode | ActionNode
