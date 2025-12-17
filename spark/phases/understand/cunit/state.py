from typing import Optional
from pathlib import Path

from pydantic import BaseModel, Field

from spark.phases.understand.cunit.models import IntentionProjection, Concept

class CUnitState(BaseModel):
    """
    Incoming intent
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


def cunit_save_state(cunit: CUnitState, version: str):
    Path(f"dumps/cunit/{version}.json").write_text(
        cunit.model_dump_json(indent=2),
        encoding="utf-8"
    )

def cunit_load_state(version: str) -> CUnitState:
    content = Path(f"dumps/cunit/{version}.json").read_text(encoding="utf-8")
    state = CUnitState.model_validate_json(content)
    return state

