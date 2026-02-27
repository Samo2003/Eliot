from dataclasses import dataclass
from pathlib import Path
from src.DAG.actions.change_state import ChangeState
from src.generator.config import GeneratorContext
from src.DAG import DAG
from .nodes import collect_nodes
from .cases import get_cases
from .states import process_state_nodes

@dataclass(frozen=True)
class DAGProcessor():
    generated_dir: Path
    traits_name: str

    def process(self, dag: DAG) -> GeneratorContext:
        # Collect nodes from DAG that need to be generated
        collected_conditions, collected_actions, state_nodes, collected_generators = collect_nodes(dag.root)

        # Only generate calendar if at least one action requires it
        require_calendar = any(action.calendar() for action in collected_actions)

        # Only include time if at least one node requires it
        require_time = require_calendar or any(
            action.time() 
            for action in collected_actions
        ) or any(
            condition.time() 
            for condition in collected_conditions
        )

        # Get context list of cases
        cases = get_cases(dag)

        # Verify state nodes, ChangeState actions and attach references for generating
        process_state_nodes(
            state_nodes, 
            [
                node 
                for node in collected_actions 
                if isinstance(node, ChangeState)
            ],
            cases
        )

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
