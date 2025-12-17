from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from spark.models import ContentSection, FollowupTopic
from spark.phases.connect.punit.models import PlannedTask
from spark.phases.understand.cunit.models import IntentionProjection, Concept



class LLMExecState(BaseModel):

    """
    Intention
    """
    intent: str

    """
    Incoming intent projection
    """
    intent_projection: Optional[IntentionProjection] = None

    """
    Planned tasks
    """
    planned_tasks: list[PlannedTask] = Field(default_factory=list)

    """
    Selected tasks
    """
    selected_tasks: list[PlannedTask] = Field(default_factory=list)

    """
    Question to be examined by the model
    """
    question: Optional[str] = None

    """
    Content sections
    """
    content: list[ContentSection] = Field(default_factory=list, description="Response content sections")

    """
    Followup topics
    """
    followup_topics: list[FollowupTopic] = Field(default_factory=list, description="Followup topics")

    """
    Reflections
    """
    reflections: list[str] = Field(default_factory=list, description="Reflections text")


def llm_exec_save_state(llm_exec: LLMExecState, version: str):
    Path(f"dumps/llm_exec/{version}.json").write_text(
        llm_exec.model_dump_json(indent=2),
        encoding="utf-8"
    )

def llm_exec_load_state(version: str) -> LLMExecState:
    content = Path(f"dumps/llm_exec/{version}.json").read_text(encoding="utf-8")
    state = LLMExecState.model_validate_json(content)
    return state
