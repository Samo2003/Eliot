from __future__ import annotations
import json
from pydantic import BaseModel, model_validator
from typing import Literal
from Guard import Guard
from Action import Action

class ActionNode(BaseModel):
    type: Literal["action"]
    final: bool = False
    action: Action
    next: GuardNode | ActionNode | None = None

    @model_validator(mode="after")
    def check_next_vs_final(self):
        if self.final and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.final and self.next is None:
            raise ValueError("Non final action node requieres next node")
        return self

class GuardNode(BaseModel):
    guardType: Literal["guard"]
    guard: Guard
    if_true: GuardNode | ActionNode
    if_false: GuardNode | ActionNode


class DAG(BaseModel):
    root: GuardNode | ActionNode

print(json.dumps(DAG.model_json_schema(), indent=4))

