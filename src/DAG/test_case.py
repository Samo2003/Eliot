from typing import List, Literal
from pydantic import BaseModel
from guard import Guard
from action import Action

class Rule(BaseModel):
    type: Literal["all", "any"]
    guards: List[Guard]
    actions: List[Action]

class TestCase(BaseModel):
    defaultAction: Literal["finish", "drop"]
    rules: List[Rule]
    

# import json
# print(json.dumps(TestCase.model_json_schema(), indent=4))
