from typing import Optional

from pydantic import BaseModel, Field

from spark.models import ContentSection, FollowupTopic
from spark.phases.connect.punit.models import PlannedTask
from spark.phases.understand.cunit.models import IntentionProjection, Concept


class ServicePhaseState(BaseModel):
    """
    Intention
    """
    intent: str

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
    Followup topics
    """
    followup_topics: list[FollowupTopic] = Field(default_factory=list, description="Followup topics")

    """
    The next task selected for execution
    """
    selected_task: Optional[PlannedTask] = None

    """
    Executor selected for the selected task
    """
    selected_executor: Optional[str] = None

    """
    Reflections
    """
    reflections: list[str] = Field(default_factory=list)
