from abc import ABC
from pydantic import BaseModel

class DAGNode(BaseModel, ABC):
    """
    Base abstract class for all DAG nodes.

    This class allows all node type to be
    treated uniformly within the DAG.
    """

    def __hash__(self) -> int:
        """
        Allows DAG nodes to be used in sets.
        """

        return id(self)
