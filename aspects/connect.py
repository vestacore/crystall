
import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from exec_prompt import exec_prompt
from spark.phases.connect.punit.models import ProcessPlannerResponse


def connect_aspect():
    print("Phase: connect")
    
    meta = {
        "id": "connect",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: connect")

        response = await exec_prompt(
            prompt_name = "spark/connect_plan_tasks",
            intent = state.intent,
            response_model = ProcessPlannerResponse,
            intent_projection = state.intent_projection
        )

        state_update = {
            "reflections": response.reflections,
            "planned_tasks": response.planned_tasks,
            "selected_tasks": [task for task in response.planned_tasks if task.type == "internal"]
        }

        return state_update
    
    return meta, handler
