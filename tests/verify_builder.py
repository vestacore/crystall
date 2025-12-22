import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from builder import SpiralBuilder
from dialog.state import DialogState
from persistence.persistence_layer import PersistenceLayer

# Mock state
class MockState(DialogState):
    # Depending on DialogState definition, we might need fields.
    # checking dialog/state.py, it has: intent, intention_descriptor, learned_facts, spark
    pass


# Mock Handlers
async def mock_handler_1(state: DialogState, persistence: PersistenceLayer):
    print("Handler 1 executing")
    # Return empty list for learned_facts
    return {"learned_facts": []}

async def mock_handler_2(state: DialogState, persistence: PersistenceLayer):
    print("Handler 2 executing")
    # Return None for intention_descriptor or just some valid update
    # Let's say we update nothing important but return valid keys
    return {}

async def mock_handler_3(state: DialogState, persistence: PersistenceLayer):
    print("Handler 3 executing")
    return {}

# Mock Factories
def factory_1():
    return mock_handler_1

def factory_2():
    return mock_handler_2

def factory_3():
    return mock_handler_3

async def main():
    print("Starting verification...")
    
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
    initial_state = DialogState(intent="test intent")
    
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
