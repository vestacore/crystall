
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

from units.project_intent.handler import project_intent
from units.extract_concepts.handler import extract_concepts

def understand_aspect():
    print("Phase: understand")
    
    meta = {
        "id": "understand",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: understand")

        projection = await project_intent(state.intent)

        concepts = await extract_concepts(
            intent = state.intent,
            projection = projection
        )

        state_update = {
            "intent_projection": projection,
            "concepts": concepts,
        }

        return state_update
    
    return meta, handler
