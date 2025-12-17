from langgraph.constants import END
from langgraph.graph import StateGraph

from spark.state import SparkState


def build_responsibility_graph():
    """
    Role: to give the user a “feedback” lever so that the system not only serves but also learns to be responsible.

    - Response evaluation (ratings, tags: “incomplete,” “ethical issue,” “accurate/inaccurate,” “important to save as a case”).
    - If desired, a short comment from the user: “what was OK/what was not.”
    - This data should influence:
        locally — subsequent responses within the session,
        globally — adjustment of settings/profiles/frames.

    Units:
        person — key actor
        punit — takes feedback as a signal: where to adjust the sequence, which prompts/profiles to update.
        cunit — can rethink conceptual frameworks (for example, the user constantly notes that the
                assistant is too technical — this is a conceptual correction).
        funit — writes feedback to the “feedback store” and initiates an update of meta-settings.

    In LangGraph: human node + feedback node → update of state/parameters.
    """
    workflow = StateGraph(SparkState)

    workflow.add_node("cunit", cunit_handler)

    workflow.set_entry_point("cunit")
    workflow.add_edge("cunit", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_responsibility_flow"

    return app_graph


async def cunit_handler(state: SparkState):
    print("- Responsibility:CUnit")

    return {
    }
