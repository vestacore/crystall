
from spark.state import SparkState
from persistence.persistence_layer import PersistenceLayer

from units.examine_question.handler import examine_question
from units.content_summary.handler import content_summary


def service_aspect():
    print("Phase: service")
    
    meta = {
        "id": "service",
        "events": ["phase.enter"],
    }

    async def handler(state: SparkState, persistence: PersistenceLayer):
        print("Phase: service")

        content = []
        reflections = []
        followup_topics = []

        for task in state.selected_tasks:
            question = task.text

            print("   Examining task: ", question)

            response = await examine_question(
                initial_intent = state.intent,
                intent_projection = state.intent_projection,
                question = question
            )

            content.append(response.content)
            reflections.extend(response.reflections)
            followup_topics.extend(response.followup_topics)

        summary = await content_summary(
            initial_intent = state.intent,
            intent_projection = state.intent_projection,
            content = content
        )

        state_update = {
            "content": content,
            "reflections": reflections,
            "followup_topics": followup_topics,
            "summary": summary
        }

        return state_update
    
    return meta, handler