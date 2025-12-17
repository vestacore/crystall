from typing import Literal

from langgraph.constants import END
from langgraph.graph import StateGraph

from spark.phases.service.funits.llm.graph import build_llm_executor_graph
from spark.phases.service.state import ServicePhaseState

def input_mapper(parent_state: ServicePhaseState):

    return {
        "intent": parent_state.intent,
        "intent_projection": parent_state.intent_projection,
        "question": parent_state.selected_task.text
    }


def build_service_graph():
    """
    Role: to accomplish the objective for which the entire endeavor was initiated.

    - Plan execution: calls to LLM, RAG, search, external APIs, human intervention.
    - Handling of branches/errors/timeouts.
    - Collection of intermediate artifacts (raw results, reasoning responses, explanations).

    Units:
        funit — the main player, executes the steps of the plan.
        punit — orchestrates: in what order, under what conditions, when to stop.
        cunit — can be connected if the plan needs to be rethought during execution (for example,
                the answers have significantly changed the context).

    In LangGraph, this is the main “execution graph”: a graph of tool nodes, LLM nodes, human nodes,
    with the ability to suspend/resume.
    """
    workflow = StateGraph(ServicePhaseState)

    workflow.add_node("select_task", select_task_handler)
    workflow.add_node("exec_llm_examine", input_mapper | build_llm_executor_graph())

    workflow.set_entry_point("select_task")

    workflow.add_conditional_edges(
        "select_task",
        select_executor_handler,
        {
            "llm": "exec_llm_examine",
            "none": END
        }
    )

    workflow.add_edge("exec_llm_examine", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_service_flow"

    return app_graph


async def select_task_handler(state: ServicePhaseState):
    print("- Service:Select task")

    if len(state.selected_tasks) == 0:
        return {
            "selected_task": None
        }
    else:
        return {
            "selected_task": state.selected_tasks.pop(0)
        }

def select_executor_handler(state: ServicePhaseState) -> Literal["llm", "none"]:
    print("- Service:Select task")

    if state.selected_task is None:
        return "none"
    else:
        if state.selected_task.type == "external":
            return "none"
        else:
            return "llm"
