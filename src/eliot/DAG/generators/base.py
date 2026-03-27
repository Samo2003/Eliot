from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Generic, final
from pydantic import model_validator
from eliot.DAG.dag_base_model import DAGBaseModel

# Generic type parameter for generator identifier
T = TypeVar("T", bound=str)

# Generic type parameter for numeric value type
N = TypeVar("N", int, float)

class ValueGeneratorBase(DAGBaseModel, Generic[T, N], ABC):
    """
    Abstract base class for runtime value generators used in DAG.
    """

    # Restore hash implementation removed by Generic inheritance
    __hash__ = DAGBaseModel.__hash__

    # Discriminator used by Pydantic for polymorphic parsing
    generatorType: T

    # Optional numeric bounds
    min: N
    max: N | None = None

    # If True, value is generated once and reused
    once: bool = False

    # Optional deterministic seed
    seed: int | None = None
    
    @model_validator(mode="before")
    def default_min(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "min" not in values:
            values["min"] = 0
        return values

    @model_validator(mode="after")
    def check_min(self) -> ValueGeneratorBase[T, N]:
        """
        Validate generator configuration.
        """
        if self.min < 0:
            raise ValueError(f"minimum value has to be 0 or greater")
        if self.max is not None and self.min > self.max:
            raise ValueError("Generator cannot produce values")
        if self.seed is not None and self.seed < 0:
            raise ValueError("Seed value has to be a positive integer")
        return self

    @final
    def __str__(self) -> str:
        """Returns string representations of generator"""
        return self.cpp_type()
    
    @final
    def cpp_type_base(self) -> str:
        """Returns common generator base name"""
        return (
            f"{self.generatorType}Generator_"
            f"{self.N_to_str(self.min)}_"
            f"{self.N_to_str(self.max)}_"
            f"{self.once}_"
            f"{self.seed}"
        )
    
    @abstractmethod
    def value(self) -> N:
        """
        Produce deterministic value when `once=True`.

        Subclasses must define how a single value is computed.
        """
        pass

    @final
    def apply_factor(self, factor: int) -> None:
        """
        Scale numeric attributes by given factor.

        Used for unit normalization.
        """
        
        self.min *= factor
        if self.max is not None:
            self.max *= factor

        self._apply_factor_inner(factor)

    @abstractmethod
    def _apply_factor_inner(self, factor: int) -> None:
        """
        Apply scaling to generator-specific parameters.
        Must be implemented by subclasses.
        """
        pass 

    @final
    def N_to_str(self, x: float | int | None) -> str:
        """
        Convert numeric value into C++-safe string fragment.

        Floating points are normalized by replacing '.' with '_'.
        """
        return str(x).replace('.', '_')
    
    @final
    def cpp_call(self) -> str:
        if self.is_state():
            return f"({self.cpp_name()}"
        return super().cpp_call()
    
    @final
    def seed_value(self) -> int:
        """
        Return deterministic seed value if provided,
        otherwise fallback to default random seed.
        """
        if self.seed is not None:
            return self.seed
        return super().seed_value()
    
    @final
    def clamp(self, x: float) -> float:
        """
        Clamps given value based on min and max
        """
        if x < self.min:
            x = self.min
        if self.max is not None and x > self.max:
            x = self.max
        return x
