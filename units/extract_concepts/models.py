from pydantic import BaseModel, Field

class Concept(BaseModel):
    """Concept descriptor."""
    id: str = Field(..., description="Concept id in snake case")
    name: str = Field(..., description="Concept name.")
    description: str = Field(..., description="Concept description.")
    confidence_score: str = Field(..., description="Confidence score")
    importance_score: str = Field(..., description="Concept importance score")

class Concepts(BaseModel):
    """Extracted concepts."""
    concepts: list[Concept] = Field(default_factory=list, description="Concepts list")
    system_response: str = Field(..., description="System level response.")

