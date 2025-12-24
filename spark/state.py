from typing import Optional
from pathlib import Path

from pydantic import BaseModel, Field

from spark.models import TextResponse, ContentSection, FollowupTopic
from spark.phases.connect.punit.models import PlannedTask
from spark.phases.understand.cunit.models import IntentionProjection, Concept
    
class SparkState(BaseModel):
    """ 
    Intention
    """
    intent: str

    """
    Intention descriptor
    """
    meta_intention_descriptor: Optional[IntentionDescriptor] = None

    """
    Learned facts
    """
    meta_learned_facts: list[LearnedFact] = Field(default_factory=list, title="Learned facts")

    """
    Incoming intent projection
    """
    intent_projection: Optional[IntentionProjection] = None

    """
    Concepts extracted from intent
    """
    concepts: list[Concept] = Field(default_factory=list)

    """
    Planned tasks
    """
    planned_tasks: list[PlannedTask] = Field(default_factory=list)

    """
    Selected tasks
    """
    selected_tasks: list[PlannedTask] = Field(default_factory=list)

    """
    Content sections
    """
    content: list[ContentSection] = Field(default_factory=list, description="Response content sections")

    """
    Content summary
    """
    summary: Optional[TextResponse] = None

    """
    Followup topics
    """
    followup_topics: list[FollowupTopic] = Field(default_factory=list, description="Followup topics")

    """
    Reflections
    """
    reflections: list[str] = Field(default_factory=list)


def spiral_save_state(cunit: SparkState, version: str):
    Path(f"../dumps/spiral/{version}.json").write_text(
        cunit.model_dump_json(indent=2),
        encoding="utf-8"
    )

def spiral_load_state(version: str) -> SparkState:
    content = Path(f"../dumps/spiral/{version}.json").read_text(encoding="utf-8")
    state = SparkState.model_validate_json(content)
    return state
