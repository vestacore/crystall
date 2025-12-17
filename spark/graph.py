
from langgraph.graph import StateGraph, END

from spark.phases.learn.graph import build_learn_graph
from spark.phases.understand.graph import build_understand_graph
from spark.phases.connect.graph import build_connect_graph
from spark.phases.service.graph import build_service_graph
from spark.phases.knowledge.graph import build_knowledge_graph
from spark.phases.evolution.graph import build_evolution_graph
from spark.phases.responsibility.graph import build_responsibility_graph

from spark.state import SparkState

def build_spark_graph():
    workflow = StateGraph(SparkState)

    workflow.add_node("learn", build_learn_graph())
    workflow.add_node("understand", build_understand_graph())
    workflow.add_node("connect", build_connect_graph())
    workflow.add_node("service", build_service_graph())
    workflow.add_node("knowledge", build_knowledge_graph())
    workflow.add_node("evolution", build_evolution_graph())
    workflow.add_node("responsibility", build_responsibility_graph())

    workflow.set_entry_point("learn")

    workflow.add_edge("learn", "understand")
    workflow.add_edge("understand", "connect")
    workflow.add_edge("connect", "service")
    workflow.add_edge("service", "knowledge")
    workflow.add_edge("knowledge", "evolution")
    workflow.add_edge("evolution", "responsibility")
    workflow.add_edge("responsibility", END)

    app_graph = workflow.compile()
    app_graph.name = "spark_flow"

    return app_graph
