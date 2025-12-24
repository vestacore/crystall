from abc import ABC, abstractmethod



class PersistenceLayer(ABC):
    @abstractmethod
    def add_spark_state(self, spark_state) -> None:
        """Add spark state into the persistence layer"""
        pass

    @abstractmethod
    def add_spark_content(self, content) -> None:
        """Add spark content sections into the persistence layer"""
        pass