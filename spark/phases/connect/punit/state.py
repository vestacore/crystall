from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from spark.phases.understand.cunit.models import IntentionProjection, Concept
from spark.phases.connect.punit.models import PlannedTask


class PUnitState(BaseModel):

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
    Reflections
    """
    reflections: list[str] = Field(default_factory=list)


def punit_save_state(punit: PUnitState, version: str):
    Path(f"dumps/punit/{version}.json").write_text(
        punit.model_dump_json(indent=2),
        encoding="utf-8"
    )

def punit_load_state(version: str) -> PUnitState:
    content = Path(f"dumps/punit/{version}.json").read_text(encoding="utf-8")
    state = PUnitState.model_validate_json(content)
    return state

