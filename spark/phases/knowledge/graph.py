from langgraph.constants import END
from langgraph.graph import StateGraph

from exec_prompt import exec_prompt
from spark.models import TextResponse
from spark.state import SparkState


def build_knowledge_graph():
    """
    Role: Turn a one-time response into system experience and show the user the way.

    - Recording artifacts in the database:
        response,
        reasoning chain (in a secure form),
        sources used,
        links to concepts/intentions.

    - Update ontology graph/semantic maps (if you have them).
    - Display in UI:
        step traces,
        which databases were used,
        which decisions the assistant made.

    Units:
        funit — actually writes to databases (RAG, graph, log).
        cunit — can repackage the result in a conceptual form (which nodes/connections to add/update).
        punit — decides what exactly is saved and in what format.

    In LangGraph: final nodes write_artifact, update_memory, log_trace.
    """
    workflow = StateGraph(SparkState)

    workflow.add_node("summary", summary_handler)

    workflow.set_entry_point("summary")
    workflow.add_edge("summary", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_knowledge_flow"

    return app_graph


async def summary_handler(state: SparkState):
    print("- Knowledge:Summary")

    response = await exec_prompt(
        prompt_name = "spark/knowledge_summary",
        intent = state.intent,
        response_model= TextResponse,
        intent_projection = state.intent_projection,
        content = state.content
    )

    return {
        "summary": response
    }
