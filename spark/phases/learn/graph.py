from langgraph.graph import StateGraph, END

from spark.state import SparkState

def build_learn_graph():
    """
    Role: prepare the stage for everything else.

    - Classify the type of request (dialogue, RAG, planning, meta-question about the system, code,
      introspection, etc.).
    - Select/collect a prompt package for this type (boundaries, styles, system prompts, tools used).
    - Set hard boundaries (ethics, policy, privacy) and user context.

    Units:
        cunit — understands “what this request is essentially about.”
        punit — selects a profile/mode and configures the graph.
        funit is not yet included — only minimal execution (classifier, router).
    """

    workflow = StateGraph(SparkState)

    workflow.add_node("cunit", cunit_handler)

    workflow.set_entry_point("cunit")
    workflow.add_edge("cunit", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_learn_flow"

    return app_graph

async def cunit_handler(state: SparkState):
    print("- Meta classify")

    return {
    }
