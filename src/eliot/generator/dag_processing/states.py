from eliot.DAG.actions.change_state import ChangeState
from eliot.DAG import StateNode
from .types import Case, StateCase

def process_state_nodes(
    state_nodes: set[StateNode],
    actions: list[ChangeState],
    cases: list[Case]
) -> None:
    """
    Post-processing step for state machine nodes.

    This function:
    1. Validates uniqueness of StateNode identifiers.
    2. Links StateNode definitions with their corresponding StateCase.
    3. Verifies semantic correctness of ChangeState actions.
    4. Enriches ChangeState actions with resolved C++ type information.

    Args:
        state_nodes: set of state nodes
        actions: set of actions
        cases: set of flattened DAG nodes into cases
    """

    def find_case(id: str) -> StateCase:
        """
        Locate the corresponding StateCase in the flattened IR model.

        Args:
            id: StateNode identifier
        """
        for case in cases:
            if case["type"] != "StateCase":
                continue
            if case["state_node"].id == id:
                return case

        raise RuntimeError(
            f"StateCase not found for StateNode with id: {id}"
        )

    # Build ID -> StateNode mapping and ensure uniqueness
    state_node_map: dict[str, StateNode] = {}
    for node in state_nodes:
        if node.id in state_node_map:
            raise ValueError(f"Duplicate StateNode id detected: {node.id}")
        state_node_map[node.id] = node

        # Attach transition identifiers to StateNode model
        node.attach_transition_ids(find_case(node.id))
    
    used_state_nodes: set[str] = set()
    used_states: dict[str, set[str]] = {node.id: set() for node in state_nodes}

    # Validate ChangeState action references
    for action in actions:
        # Verify that referenced StateNode exists
        if action.target not in state_node_map:
            raise ValueError(
                f"Undefined reference to state node in ChangeState action: {action.target}"
            )

        target_node = state_node_map[action.target]

        # Mark state node as used
        used_state_nodes.add(action.target)

        # Mark target state as used
        used_states[action.target].add(action.state)

        # Verify that target state is defined in the StateNode
        if action.state not in target_node.states:
            raise ValueError(
                f"Cannot set undefined state {action.state} to StateNode with id: {target_node.id}"
            )

        # Attach resolved C++ type name to action for code generation
        action.state_cpp_type = target_node.cpp_type

    # Check for unused state nodes
    unused = set(state_node_map.keys()) - used_state_nodes
    if unused:
        raise ValueError(
            f"Unused StateNode definitions detected: {', '.join(sorted(unused))}"
        )

    # Validate all defined states are reachable
    for node_id, node in state_node_map.items():
        defined_states = set(node.states)
        reachable_states = used_states[node_id] | {node.initial}

        unreachable = defined_states - reachable_states
        if unreachable:
            raise ValueError(
                f"StateNode '{node_id}' contains unreachable states: "
                f"{', '.join(sorted(unreachable))}"
            )
