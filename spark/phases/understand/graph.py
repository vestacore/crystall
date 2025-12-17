from langgraph.constants import END
from langgraph.graph import StateGraph

from spark.phases.understand.cunit.graph import build_cunit_graph
from spark.state import SparkState


def build_understand_graph():
    """
    Role: translate the request into semantic geometry.

    - Identify the intention and project it onto semantic vectors
      (Truth/Deep/Unity/Service/Knowledge/Evolution/Accountability).
    - Identify concepts, their connections, and limitations.
    - Normalization: “What does the user really want?”,
      “What is the minimum question we need to solve in this iteration?”.

    Units:
        cunit — the main actor, builds conceptual frameworks.
        punit — decides: whether to ask clarifying questions, branch the plan, make a deferred graph.
        funit — performs individual steps (LLM call for analysis/reflection).

    In LangGraph: one or more “analysis/extract_intent” nodes, possibly with a “ask the user → update understanding”
    cycle.
    """
    workflow = StateGraph(SparkState)

    workflow.add_node("cunit", build_cunit_graph())

    workflow.set_entry_point("cunit")
    workflow.add_edge("cunit", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_understand_flow"

    return app_graph

