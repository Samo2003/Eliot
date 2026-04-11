from typing import Any, ClassVar
from pydantic import TypeAdapter
from eliot.DAG.actions import Action
from eliot.DAG.conditions import Condition
from .node import DAGNode
from .action import ActionNode
from .decision import DecisionNode
from .state import StateNode, Transition

class DAGNodeFactory:
    """
    Factory class responsible for constructing DAGNode instances
    from raw dictionary data.

    It determines the correct node type based on keys present
    in the input structure and recursively builds the DAG.
    """

    # Adapter for validating Action definitions
    _action_adapter: ClassVar[TypeAdapter[Action]] = TypeAdapter(Action)
    
    # Adapter for validating Condition definitions
    _condition_adapter: ClassVar[TypeAdapter[Condition]] = TypeAdapter(Condition)
    
    @staticmethod
    def create(data: dict[str, Any]) -> DAGNode:
        """
        Create a DAGNode from raw dictionary data.
        If the input is already a DAGNode, it is returned as-is.

        Raises:
            ValueError if structure does not match any known node type.
        """
        if isinstance(data, DAGNode):
            return data

        if "action" in data:
            return DAGNodeFactory._create_action(data)

        if "condition" in data:
            return DAGNodeFactory._create_decision(data)

        if "transitions" in data:
            return DAGNodeFactory._create_state(data)

        raise ValueError(f"Unknown node structure: {data}")
    
    @staticmethod
    def _create_action(data: dict[str, Any]) -> ActionNode:
        """
        Create an ActionNode.

        - Validates the action using TypeAdapter
        - Recursively constructs the next node if present
        """
        next_node = data.get("next")

        return ActionNode(
            action=DAGNodeFactory._action_adapter.validate_python(data["action"]),
            next=DAGNodeFactory.create(next_node) if next_node else None
        )
        
    @staticmethod
    def _create_decision(data: dict[str, Any]) -> DecisionNode:
        """
        Create a DecisionNode.

        - Validates the condition using TypeAdapter
        - Recursively constructs both branches
        """
        return DecisionNode(
            condition=DAGNodeFactory._condition_adapter.validate_python(data["condition"]),
            if_true=DAGNodeFactory.create(data["if_true"]),
            if_false=DAGNodeFactory.create(data["if_false"])
        )
        
    @staticmethod
    def _create_state(data: dict[str, Any]) -> StateNode:
        """
        Create a StateNode.

        - Iterates through transitions
        - Recursively builds target nodes
        - Wraps each transition in a Transition object
        """
        transitions_data: dict[str, dict[str, Any]] = data.get("transitions", {})

        transitions: dict[str, Transition] = {
            state: Transition(
                next=DAGNodeFactory.create(t["next"])
            )
            for state, t in transitions_data.items()
        }

        return StateNode(
            id=data["id"],
            initial=data["initial"],
            transitions=transitions
        )
