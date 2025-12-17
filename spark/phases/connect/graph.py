from langgraph.constants import END
from langgraph.graph import StateGraph

from spark.phases.connect.punit.graph import build_punit_graph
from spark.state import SparkState


def build_connect_graph():
    """
    Role: decide where exactly to go for data/actions.

    - Select relevant vectors (which databases, which indexes, which APIs).
    - Configure the tool layer: which RAG clusters, which systems (incidents, logs, documents, music, etc.).
    - Possibly — building a microplan: what steps need to be taken sequentially (for example: first RAG, then web, then local history).

    Units:
        cunit — understands which semantic fields are affected.
        punit — “stitches” this into a process: selects specific repositories and tools.
        funit — can do a “dry run”/preflight (availability check, query adaptation).

    In LangGraph: node of the “select_tools / select_stores / build_query_plan” level.
    """
    workflow = StateGraph(SparkState)

    workflow.add_node("punit", build_punit_graph())

    workflow.set_entry_point("punit")
    workflow.add_edge("punit", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_connect_flow"

    return app_graph

