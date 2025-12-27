from typing import Optional
from pydantic import BaseModel, Field

class PlannedTask(BaseModel):
    """
    Task type
    """
    type: str = Field(..., description="external - select data from external systems like rag or api / user - ask user question / internal - internal question for the model")

    """
    Question or action text
    """
    text: Optional[str] = Field(..., description="Carefully formulated action description ( in case of external task type) or query text ( in case of user/internal task type)")

    """
    Confidence score
    """
    confidence: int= Field(..., description="Confidence score between 0 and 100")

    """
    Importance score
    """
    importance: int= Field(..., description="Importance score between 0 and 100")


class ProcessPlannerResponse(BaseModel):
    """
    Reflections
    """
    reflections: list[str] = Field(default_factory=list, description="Reflections text")

    """
    Planned tasks
    """
    planned_tasks: list[PlannedTask] = Field(default_factory=list, description="Planned tasks list")

