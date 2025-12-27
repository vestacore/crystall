
import asyncio
from unittest.mock import MagicMock

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

from aspects.meta_learn import meta_learn_aspect
from aspects.meta_deep import meta_deep_aspect
from aspects.understand import understand_aspect
from aspects.connect import connect_aspect
from aspects.service import service_aspect


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