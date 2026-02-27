import yaml
import json
from src.DAG import DAG
from src.test_case import translate_to_DAG, load_test_case
from .builder import Builder
from .config import GeneratorConfig
from .dag_processing.processor import DAGProcessor
from .generators import GeneratorBase

class Generator():
    def __init__(self, config: GeneratorConfig):
        self._cfg = config
        self._builder = Builder(self._cfg)
        self._processor = DAGProcessor(
            generated_dir=self._builder.generated_dir,
            traits_name=self._cfg.traits_path.name
        )

    def run(self) -> None:
        if self._cfg.print_schema:
            print(json.dumps(DAG.model_json_schema(), indent=4))
            return
        
        self._builder.clear_generated_dir()

        dag = self._load_dag()

        self._generate(dag)

        self._builder.build()

    def _load_dag(self) -> DAG:
        """
        Loads DAG model directly if provided otherwise loads and translates given test case

        Raises `RuntimeError` if loading fails
        """

        try:
            if self._cfg.dag_path:
                # Get file extension to determine type
                ext = self._cfg.dag_path.suffix.lower()
                # Load and validate DAG
                with open(self._cfg.dag_path, "r", encoding="utf-8") as file:
                    if ext == ".yaml":
                        data = yaml.safe_load(file)
                    elif ext == ".json":
                        data = json.load(file)
                    else:
                        raise ValueError(f"Unsupported file type: {ext}")
                    return DAG.model_validate(data)
            elif self._cfg.test_case_path:
                # Load and convert test case into DAG
                test_case_model = load_test_case(self._cfg.test_case_path)
                return translate_to_DAG(test_case_model)
            else:
                raise RuntimeError("No input path provided")
        except Exception as e:
            raise RuntimeError(f"ERROR: loading input file: {e}")

    def _generate(self, dag: DAG) -> None:
        """Main generator function handling generating"""

        context = self._processor.process(dag)

        # Generate necessary files
        for generator in GeneratorBase.registry:
            generator.generate(context)
