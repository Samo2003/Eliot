from dataclasses import dataclass
from pathlib import Path
from src.DAG.actions.change_state import ChangeState
from src.generator.config import GeneratorContext
from src.DAG import DAG
from .nodes import collect_nodes
from .cases import get_cases
from .states import process_state_nodes

@dataclass(frozen=True)
class DAGProcessor:
    """
    Responsible for transforming a validated DAG model into an
    intermediate representation (GeneratorContext) used for
    code generation.
    """

    generated_dir: Path
    traits_name: str

    def process(self, dag: DAG) -> GeneratorContext:
        """
        Convert DAG into GeneratorContext.

        This method performs semantic analysis and prepares all
        information required by the generation phase.

        Args:
            dag: Parsed and validated DAG specification

        Returns:
            Prepared GeneratorContext
        """

        # Collect all unique nodes required for generation
        collected_conditions, collected_actions, state_nodes, collected_generators = collect_nodes(dag.root)

        # Collect all unique nodes required for generation
        require_calendar = any(action.calendar() for action in collected_actions)

        # Determine whether time support is required
        require_time = require_calendar or any(
            action.time() 
            for action in collected_actions
        ) or any(
            condition.time() 
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
                if isinstance(node, ChangeState)
            ],
            cases
        )

        # Perform semantic validation and state linking
        return GeneratorContext(
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
