from abc import ABC, abstractmethod

from dialog.state import SparkContent
from spark.state import SparkState


class PersistenceLayer(ABC):
    @abstractmethod
    def add_spark_state(self, spark_state: SparkState) -> None:
        """Add spark state into the persistence layer"""
        pass

    @abstractmethod
    def add_spark_content(self, content: list[SparkContent]) -> None:
        """Add spark content sections into the persistence layer"""
        pass