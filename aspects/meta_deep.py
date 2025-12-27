
import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from exec_prompt import exec_prompt
from dialog.models import IntentionDescriptor



def meta_deep_aspect():
    print("Meta: deep")
    
    meta = {
        "id": "meta.deep",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Meta: deep")

        response = await exec_prompt(
            prompt_name = "dialog/deep_classify",
            intent = state.intent,
            response_model = IntentionDescriptor
        )

        state_update = {
            "meta_intention_descriptor": response,
        }

        return state_update
    
    return meta, handler

