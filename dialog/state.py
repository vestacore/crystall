from typing import Optional
from pathlib import Path

from pydantic import BaseModel, Field

from dialog.models import IntentionDescriptor, LearnedFact
from spark.models import ContentSection
from spark.state import SparkState


class SparkContent(BaseModel):
    """encapsulates reference to the content section"""

    """
    Content produced by Spark
    """
    content: ContentSection

    """
    Spark state reference
    """
    spark_state: SparkState


class DialogState(BaseModel):
    """
    Meta information related to the processing of the Spark
    """

    """
    The last intention accepted by the agent
    """
    intent: str

    """
    Intention descriptor
    """
    intention_descriptor: Optional[IntentionDescriptor] = None

    """
    Learned facts
    """
    learned_facts: list[LearnedFact] = Field(default_factory=list, title="Learned facts")

    """
    Spark being processed
    """
    spark: Optional[SparkState] = None




def dialog_save_state(state: DialogState, version: str):
    Path(f"dumps/dialog/{version}.json").write_text(
        state.model_dump_json(indent=2),
        encoding="utf-8"
    )

def dialog_load_state(version: str) -> DialogState:
    content = Path(f"dumps/dialog/{version}.json").read_text(encoding="utf-8")
    state = DialogState.model_validate_json(content)
    return state
