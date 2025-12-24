
import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer


def meta_learn_aspect():
    print("Meta: learn")
    
    meta = {
        "id": "meta.learn",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Meta: deep")

        state_update = {
            "categories": [
                "Truth",
                "Deep",
                "Connect",
                "Knowledge",
                "Service",
                "Responsibility"
            ],
            "vectors": [
                "Knowledge",
                "Deep",
                "Connect",
                "Responsibility"
            ],
            "summary": "User wants a structured understanding of the EU DORA regulation specifically focused on how it applies to European payment service providers (PSPs). The aim is to map DORA's structure and obligations onto PSP activities and compliance responsibilities.",
            "reasoning": "The request seeks comprehension (not execution) of regulatory structure and applicability. It therefore requires sourcing and organizing factual regulatory text (Knowledge), interpreting mechanisms and obligations (Deep), connecting those obligations to PSP operations and existing frameworks (Connect), and highlighting compliance responsibilities and accountability (Responsibility). Truth is needed to ground claims; Service actions (execution) are minimal."
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

        state_update = {
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

        state_update = {
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

        state_update = {
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
    
    initial_state = SparkState(intent="test intent")
    
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