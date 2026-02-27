from typing import Dict, Set, List
from src.DAG.actions.change_state import ChangeState
from src.DAG import StateNode
from .types import Case, StateCase

def process_state_nodes(state_nodes: Set[StateNode], actions: List[ChangeState], cases: List[Case]) -> None:
    def find_case(id: str) -> StateCase:
        for case in cases:
            if case["type"] != "StateCase":
                continue
            if case["state_node"].id == id:
                return case
        raise RuntimeError(f"StateCase not found for StateNode with id: {id}")

    # Build ID to `StateNode` map and attach transition IDs
    state_node_map: Dict[str, StateNode] = {}
    for node in state_nodes:
        if node.id in state_node_map:
            raise ValueError(f"Duplicate StateNode id detected: {node.id}")
        state_node_map[node.id] = node

        # Attach transition IDs to `StateNode`
        node.attach_transition_ids(find_case(node.id))
    
    # Verify action references to StateNodes
    for action in actions:
        if action.target not in state_node_map:
            raise ValueError(f"Undefined reference to state node in ChangeState action: {action.target}")

        target_node = state_node_map[action.target]
        if action.state not in target_node.states():
            raise ValueError(f"Cannot set undefined state {action.state} to StateNode with id: {target_node.id}")

        # Attach `StateNode` to action node for generating
        action.attach_state_node_type(target_node.cpp_type())
