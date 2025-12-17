from pydantic import BaseModel, Field

class IntentionProjection(BaseModel):
    """Mapping the intention across seven semantic aspects."""
    truth: str = Field(..., description="Why this intention exists. Reveal the originating need, tension, or purpose that calls the intention into being.")
    deep: str = Field(..., description="What the intention carries within. Reveal its internal semantic layers, implicit questions, assumptions, or meaning-densities.")
    unity: str = Field(..., description="What the intention relates to. Reveal its surrounding semantic field, contextual relations, and resonance domains.")
    service: str = Field(..., description="What role this intention plays. Reveal the functional and operational purpose the intention serves within a broader process.")
    knowledge: str = Field(..., description="How the intention expresses itself. Reveal how the intention shapes information, inquiry patterns, and expressions of knowledge.")
    evolution: str = Field(..., description="What the intention can become. Reveal potential transformations, expansions, and deeper developmental trajectories.")
    accountability: str = Field(..., description="How the intention self-fulfills. Reveal how the intention maintains coherence with its purpose through internal responsibility structures.")

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

