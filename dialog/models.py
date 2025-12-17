from enum import Enum
from pydantic import BaseModel, Field


class IntentionDescriptor(BaseModel):
    categories: list[str] = Field(..., description="Categories")
    vectors: list[str] = Field(..., description="Vectors")
    summary: str = Field(..., description="Intent summary")
    reasoning: str = Field(..., description="Brief explanation of why this classification was chosen")



class LearnedFact(BaseModel):
    """
    Learned fact
    """
    truth: str = Field(..., description="What is the fact about (concept)?")
    deep: str = Field(..., description="What exactly is asserted?")
    connect: str = Field(..., description="What is this fact directly connected to?")
    service: str = Field(..., description="What is stated as the cause (if any)?")
    knowledge: str = Field(..., description="What observable effect or manifestation is stated?")
    evolution: str = Field(..., description="Is any temporal or causal progression described?")
    responsibility: str = Field(..., description="Is any response, obligation, or action implied?")


class LearnFactsResponse(BaseModel):
    learned_facts: list[LearnedFact] = Field(..., description="Learned facts")