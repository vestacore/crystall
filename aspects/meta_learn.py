import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from exec_prompt import exec_prompt
from dialog.models import IntentionDescriptor, LearnFactsResponse
from spark.phases.understand.cunit.models import IntentionProjection, Concepts
from spark.phases.connect.punit.models import ProcessPlannerResponse
from spark.models import LLMExecutorResponse



def meta_learn_aspect():
    print("Meta: learn")
    
    meta = {
        "id": "meta.learn",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Meta: learn")

        response = await exec_prompt(
            prompt_name = "dialog/learn_facts",
            intent = "Analyze request and extract direct or indirect facts from it",
            response_model = LearnFactsResponse,
            request = state.intent
        )

        state_update = {
            "meta_learned_facts": response.learned_facts,
        }

        return state_update
    
    return meta, handler
