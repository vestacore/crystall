from langgraph.graph import StateGraph, END

from spark.models import LLMExecutorResponse
from spark.phases.service.funits.llm.state import LLMExecState
from exec_prompt import exec_prompt

def build_llm_executor_graph():
    workflow = StateGraph(LLMExecState)

    workflow.add_node("execution", execution_handler)

    workflow.set_entry_point("execution")

    workflow.add_edge("execution", END)

    app_graph = workflow.compile()
    app_graph.name = "service_llm_executor"

    return app_graph

async def execution_handler(state: LLMExecState):
    print("- Execute LLM question")

    response = await exec_prompt(
        prompt_name = "spark/service_examine_question",
        intent = state.question,
        response_model = LLMExecutorResponse,
        initial_intent = state.intent,
        intent_projection = state.intent_projection
    )

    return {
        "content": response.content,
        "reflections": response.reflections,
        "followup_topics": response.followup_topics,
    }