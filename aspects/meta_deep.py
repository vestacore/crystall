
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer
from units.deep_classify.handler import deep_classify

def meta_deep_aspect():
    print("Meta: deep")
    
    meta = {
        "id": "meta.deep",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Meta: deep")

        state_update = {
            "meta_intention_descriptor": await deep_classify(state.intent),
        }

        return state_update
    
    return meta, handler

