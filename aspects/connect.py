
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

from units.plan_tasks.handler import plan_tasks


def connect_aspect():
    print("Phase: connect")
    
    meta = {
        "id": "connect",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: connect")

        response = await plan_tasks(
            intent = state.intent,
            intent_projection = state.intent_projection
        )

        state_update = {
            "reflections": response.reflections,
            "planned_tasks": response.planned_tasks,
            "selected_tasks": [task for task in response.planned_tasks if task.type == "internal"]
        }

        return state_update
    
    return meta, handler
