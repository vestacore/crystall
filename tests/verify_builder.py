import asyncio
import sys
import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from builder import SpiralBuilder
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

# Mock Handlers
async def mock_handler_1(state: SparkState, persistence: PersistenceLayer):
    print("Handler 1 executing")
    # Return valid SparkState update
    return {"meta_learned_facts": []}

async def mock_handler_2(state: SparkState, persistence: PersistenceLayer):
    print("Handler 2 executing")
    # Return empty dict which is valid update
    return {}

async def mock_handler_3(state: SparkState, persistence: PersistenceLayer):
    print("Handler 3 executing")
    return {}

# Mock Factories - Must return (meta, handler) tuple now
def factory_1():
    return {"id": "mock_1"}, mock_handler_1

def factory_2():
    return {"id": "mock_2"}, mock_handler_2

def factory_3():
    return {"id": "mock_3"}, mock_handler_3

async def main():
    print("Starting verification (verify_builder.py)...")
    
    # 1. Instantiate Builder
    builder = SpiralBuilder()
    
    # 2. Configure Graph
    builder.phase("test_phase_1") \
           .base_aspect(factory_1) \
           .aspects(factory_2) \
           .policy(max_proposals=5)
           
    builder.phase("test_phase_2") \
           .base_aspect(factory_3)
           
    # 3. Build Graph
    mock_persistence = MagicMock(spec=PersistenceLayer)
    graph = builder.build(persistence=mock_persistence)
    
    # 4. Invoke Graph
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
