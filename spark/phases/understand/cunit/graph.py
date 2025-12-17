
from langgraph.graph import StateGraph, END

from spark.phases.understand.cunit.models import IntentionProjection, Concepts
from spark.phases.understand.cunit.state import CUnitState
from exec_prompt import exec_prompt

def build_cunit_graph():
    workflow = StateGraph(CUnitState)

    # Classify intent
    workflow.add_node("project_intent", project_intent_handler)

    # Extract concepts
    workflow.add_node("extract_concepts", extract_concepts_handler)

    workflow.set_entry_point("project_intent")

    workflow.add_edge("project_intent", "extract_concepts")
    workflow.add_edge("extract_concepts", END)

    app_graph = workflow.compile()
    app_graph.name = "understand_cunit"

    return app_graph


async def project_intent_handler(state: CUnitState):
    print("- Project intent")

    response = await exec_prompt(
        prompt_name = "spark/learn_project_intent",
        intent = state.intent,
        response_model = IntentionProjection
    )

    return {
        "intent_projection": response
    }


async def extract_concepts_handler(state: CUnitState):
    print("- Extract concepts")

    response = await exec_prompt(
        prompt_name = "spark/learn_extract_concepts",
        intent = state.intent,
        response_model = Concepts,
        intent_projection = state.intent_projection
    )

    return {
        "concepts": response.concepts
    }


