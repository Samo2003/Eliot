from typing import Any
from pydantic import BaseModel, model_validator
from .nodes import DAGNode, DAGNodeFactory

class DAG(BaseModel):
    """
    Root container for the DAG specification.
    """

    # DAG root node
    root: DAGNode
    
    @model_validator(mode="before")
    @classmethod
    def parse_root(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["root"] = DAGNodeFactory.create(data["root"])
        return data
