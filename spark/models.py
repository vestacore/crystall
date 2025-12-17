from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Concept(BaseModel):
    """
    Concept name
    """
    name: str= Field(..., description="Concept name")


class ContentSection(BaseModel):

    """
    Section title
    """
    title: str= Field(..., description="Section title")

    """
    Section header
    """
    header: str= Field(..., description="Section header")

    """
    Section content
    """
    content: str= Field(..., description="Section content")

    """
    Section questions
    """
    question: str = Field(..., description="The question answered by this section")

    """
    Concepts
    """
    concepts: list[Concept] = Field(default_factory=list, description="Related concepts")


class FollowupTopic(BaseModel):

    """
    Topic name
    """
    topic: str = Field(..., description="Topic name")

    """
    Questions
    """
    questions: str = Field(..., description="Followup questions")

    """
    Concepts
    """
    concepts: list[Concept] = Field(default_factory=list, description="Related concepts")


class TextResponse(BaseModel):

    """ Response title."""
    title: str = Field(..., description="Response title")

    """ Response header."""
    header: str = Field(..., description="Response header")

    """ Response text."""
    text: str = Field(..., description="Response text")

    """ Response text summary."""
    summary: str = Field(..., description="Response text summary")

class LLMExecutorResponse(BaseModel):

    """
    Content sections
    """
    content: list[ContentSection] = Field(default_factory=list, description="Response content sections")

    """
    Reflections
    """
    reflections: list[str] = Field(default_factory=list, description="Reflections text")

    """
    Followup topics
    """
    followup_topics: list[FollowupTopic] = Field(default_factory=list, description="Followup topics")

