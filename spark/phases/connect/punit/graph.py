from langgraph.graph import StateGraph, END

from exec_prompt import exec_prompt
from spark.phases.connect.punit.models import ProcessPlannerResponse
from spark.phases.connect.punit.state import PUnitState


def build_punit_graph():
    workflow = StateGraph(PUnitState)

    # Plan tasks
    workflow.add_node("planning", planning_handler)
    workflow.add_node("selecting", select_handler)

    workflow.set_entry_point("planning")

    workflow.add_edge("planning", "selecting")
    workflow.add_edge("selecting", END)

    app_graph = workflow.compile()
    app_graph.name = "connect_punit"

    return app_graph


async def planning_handler(state: PUnitState):
    print("- Planning tasks")

    response = await exec_prompt(
        prompt_name = "spark/connect_plan_tasks",
        intent = state.intent,
        response_model = ProcessPlannerResponse,
        intent_projection = state.intent_projection
    )

    return {
        "reflections": response.reflections,
        "planned_tasks": response.planned_tasks,
    }

async def select_handler(state: PUnitState):
    print("- Selecting tasks")

    return {
        "selected_tasks": [task for task in state.planned_tasks if task.type == "internal"]
    }