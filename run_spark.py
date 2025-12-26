
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


def service_aspect():
    print("Phase: service")
    
    meta = {
        "id": "service",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: service")

        state_update = {
        }

        return state_update
    
    return meta, handler


async def main():
    print("Starting verification...")
    
    builder = SpiralBuilder()

    builder.meta_phase("learn") \
           .base_aspect(meta_learn_aspect)

    builder.meta_phase("deep") \
           .base_aspect(meta_deep_aspect)

    builder.phase("understand") \
           .base_aspect(understand_aspect)

    builder.phase("connect") \
           .base_aspect(connect_aspect)

    builder.phase("service") \
           .base_aspect(service_aspect)


    mock_persistence = MagicMock(spec=PersistenceLayer)
    graph = builder.build(persistence=mock_persistence)
    
    initial_state = SparkState(intent="I want to understand the structure of EU DORA regulation as it applies to the work of European payment service providers.")
    
    print("Invoking graph...")
    try:
        result = await graph.ainvoke(initial_state)
        print("Graph execution completed successfully.")
        print("Result:", result)
    except Exception as e:
        print(f"Graph execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())