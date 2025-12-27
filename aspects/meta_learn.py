
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

from units.learn_facts.handler import learn_facts


def meta_learn_aspect():
    print("Meta: learn")
    
    meta = {
        "id": "meta.learn",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Meta: learn")

        state_update = {
            "meta_learned_facts": await learn_facts(state.intent),
        }

        return state_update
    
    return meta, handler
