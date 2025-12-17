from pydantic import BaseModel, Field
from pathlib import Path

from dialog.models import LearnedFact
from dialog.state import SparkContent
from persistence.persistence_layer import PersistenceLayer
from spark.state import SparkState

class FilePersistenceState(BaseModel):
    """
    File persistence state
    """

    """
    Learned facts
    """
    learned_facts: list[LearnedFact] = Field(default_factory=list, title="Learned facts")

    """
    Sparks
    """
    sparks: list[SparkState] = Field(default_factory=list)

    """
    References to content sections produced by sparks
    """
    content: list[SparkContent] = Field(default_factory=list)



class FilePersistence(PersistenceLayer):

    def __init__(self, version: str):
        self.version = version
        self.state = FilePersistenceState()

    def add_spark_state(self, spark_state: SparkState) -> None:
        """Add spark state into the persistence layer"""
        pass

    def add_spark_content(self, content: list[SparkContent]) -> None:
        """Add spark content sections into the persistence layer"""
        pass

    def save_state(self):
        Path(f"../dumps/state/{self.version}.json").write_text(
            self.state.model_dump_json(indent=2),
            encoding="utf-8"
        )

    def load_state(self):
        content = Path(f"../dumps/state/{self.version}.json").read_text(encoding="utf-8")
        self.state = FilePersistenceState.model_validate_json(content)

