import yaml
import json
from src.DAG import DAG
from src.test_case import translate_to_DAG, load_test_case
from .builder import Builder
from .config import GeneratorConfig
from .dag_processing.processor import DAGProcessor
from .generators import GeneratorBase

class Generator:
    """
    Orchestration class responsible for the full code generation pipeline.
    """

    def __init__(self, config: GeneratorConfig):
        """
        Initialize generator with provided configuration
        """
        self._cfg = config
        self._builder = Builder(self._cfg)
        self._processor = DAGProcessor(
            generated_dir=self._builder.generated_dir,
            traits_name=self._cfg.traits_path.name
        )

    def run(self) -> None:
        """
        Entry point of the generation process.
        Executes the full generation pipeline.
        """

        # Print DAG JSON specification and exit
        if self._cfg.print_schema:
            print(json.dumps(DAG.model_json_schema(), indent=4))
            return
        
        # Clean output directory before generation
        self._builder.clear_generated_dir()

        # Load and validate DAG model
        dag = self._load_dag()

        # Generate source files from DAG
        self._generate(dag)

        # Build generated code
        self._builder.build()

    def _load_dag(self) -> DAG:
        """
        Loads DAG model directly if provided otherwise loads and translates given test case

        Returns:
            Parsed and validated `DAG` object.

        Raises:
            RuntimeError: if loading or validation fails
        """

        try:
            if self._cfg.dag_path:
                # Parse input file
                with open(self._cfg.dag_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)
                    
                    # Validate and construct DAG model
                    return DAG.model_validate(data)
            elif self._cfg.test_case_path:
                # Load test case and translate into DAG model
                test_case_model = load_test_case(self._cfg.test_case_path)
                return translate_to_DAG(test_case_model)

            else:
                raise RuntimeError("No input path provided")
        except Exception as e:
            # Wrap all errors into a controlled RuntimeError
            raise RuntimeError(f"ERROR: loading input file: {e}")

    def _generate(self, dag: DAG) -> None:
        """
        Core generation phase.

        Args:
            dag: Parsed and validated DAG specification
        """

        # Transform DAG into internal representation
        context = self._processor.process(dag)

        # Execute all registered code generators
        for generator_cls in GeneratorBase.registry:
            generator = generator_cls()
            generator.generate(context)
