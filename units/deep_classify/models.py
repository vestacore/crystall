from enum import Enum
from pydantic import BaseModel, Field


class IntentionDescriptor(BaseModel):
    categories: list[str] = Field(..., description="Categories")
    vectors: list[str] = Field(..., description="Vectors")
    summary: str = Field(..., description="Intent summary")
    reasoning: str = Field(..., description="Brief explanation of why this classification was chosen")


