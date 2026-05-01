from dataclasses import dataclass
from pathlib import Path
from eliot.DAG.actions.set_state import SetState
from eliot.generator.config import DAGContext
from eliot.DAG import DAG
from .nodes import collect_nodes
from .cases import get_cases
from .states import process_state_nodes

@dataclass(frozen=True)
class DAGProcessor:
    """
    Responsible for transforming a validated DAG model into an
    intermediate representation (DAGContext) used for
    code generation.
    """

    generated_dir: Path
    traits_name: str

    def process(self, dag: DAG) -> DAGContext:
        """
        Convert DAG into DAGContext.

        This method performs semantic analysis and prepares all
        information required by the generation phase.

        Args:
            dag: Parsed and validated DAG specification

        Returns:
            Prepared DAGContext
        """

        # Collect all unique nodes required for generation
        collected_conditions, collected_actions, state_nodes, collected_generators = collect_nodes(dag.root)

        # Collect all unique nodes required for generation
        require_calendar = any(action.calendar for action in collected_actions)

        # Determine whether time support is required
        require_time = require_calendar or any(
            action.time
            for action in collected_actions
        ) or any(
            condition.time
            for condition in collected_conditions
        )

        # Flatten DAG into execution cases
        cases = get_cases(dag)

        # Perform semantic validation and state linking
        process_state_nodes(
            state_nodes, 
            [
                node 
                for node in collected_actions 
                if isinstance(node, SetState)
            ],
            cases
        )

        # Perform semantic validation and state linking
        return DAGContext(
            generated_dir=self.generated_dir,
            conditions=collected_conditions,
            actions=collected_actions,
            state_nodes=state_nodes,
            generators=collected_generators,
            traits=self.traits_name,
            require_calendar=require_calendar,
            require_time=require_time,
            cases=cases
        )
