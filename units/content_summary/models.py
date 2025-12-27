
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ContentSummary(BaseModel):

    """ Response title."""
    title: str = Field(..., description="Response title")

    """ Response header."""
    header: str = Field(..., description="Response header")

    """ Response text."""
    text: str = Field(..., description="Response text")

    """ Response text summary."""
    summary: str = Field(..., description="Response text summary")