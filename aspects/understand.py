
import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from exec_prompt import exec_prompt
from spark.phases.understand.cunit.models import IntentionProjection, Concepts


def understand_aspect():
    print("Phase: understand")
    
    meta = {
        "id": "understand",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: understand")

        projection_response = await exec_prompt(
            prompt_name = "spark/learn_project_intent",
            intent = state.intent,
            response_model = IntentionProjection
        )

        concepts_response = await exec_prompt(
            prompt_name = "spark/learn_extract_concepts",
            intent = state.intent,
            response_model = Concepts,
            intent_projection = projection_response
        )

        state_update = {
            "intent_projection": projection_response,
            "concepts": concepts_response.concepts,
        }

        return state_update
    
    return meta, handler
