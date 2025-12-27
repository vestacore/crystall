

import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from exec_prompt import exec_prompt
from spark.models import LLMExecutorResponse


def service_aspect():
    print("Phase: service")
    
    meta = {
        "id": "service",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: service")

        content = []
        reflections = []
        followup_topics = []

        for task in state.selected_tasks:
            question = task.text

            print("   Examining task: ", question)

            response = await exec_prompt(
                prompt_name = "spark/service_examine_question",
                intent = question,
                response_model = LLMExecutorResponse,
                initial_intent = state.intent,
                intent_projection = state.intent_projection
            )

            content.append(response.content)
            reflections.extend(response.reflections)
            followup_topics.extend(response.followup_topics)

        state_update = {
            "content": content,
            "reflections": reflections,
            "followup_topics": followup_topics,
        }

        return state_update
    
    return meta, handler