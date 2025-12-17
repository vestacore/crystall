from __future__ import annotations

from typing import Callable, Awaitable, Tuple

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph

from dialog.models import IntentionDescriptor, LearnFactsResponse
from dialog.state import DialogState, SparkContent
from exec_prompt import exec_prompt
from persistence.persistence_layer import PersistenceLayer
from spark.graph import build_spark_graph
from spark.state import SparkState
from utils import run_graph

HandlerFunc = Callable[[DialogState, PersistenceLayer], Awaitable[dict]]

NodeFunc = Callable[[DialogState], Awaitable[dict]]

PhaseBuilderFunc = Callable[[str, HandlerFunc], None]

PhasesBuilderFunc = Callable[[PhaseBuilderFunc], None]

def phase_name(name: str):
    def decorator(func: Callable):
        func._phase_handler_name = name
        return func
    return decorator

def build_dialog_graph(phase_handlers: list[HandlerFunc], persistence: PersistenceLayer) -> CompiledStateGraph[DialogState]:
    """
    Across these phases, the Dialog keeps the journey coherent.

    It ensures that:
    - meaning accumulates instead of fragmenting,
    - intentions remain visible,
    - transitions feel natural,

    and the user never loses their place in the larger flow.
    """

    def build_node(handler: HandlerFunc) -> NodeFunc:

        async def node_wrapper(state: DialogState) -> dict:
            return await handler(state, persistence)

        return node_wrapper

    nodes: list[Tuple[str,NodeFunc]] = []

    def phase(name: str, handler: HandlerFunc):
        nodes.append((name, build_node(handler)))

    for phase_handler in phase_handlers:
        name = getattr(phase_handler, "_phase_handler_name")
        phase(name, phase_handler)

    workflow = StateGraph(DialogState)

    for node in nodes:
        workflow.add_node(node[0], node[1])

    workflow.set_entry_point(nodes[0][0])

    for current_node, next_node in zip(nodes, nodes[1:]):
        workflow.add_edge(current_node[0], next_node[0])

    workflow.add_edge(nodes[-1][0], END)

    app_graph = workflow.compile()
    app_graph.name = "dialog_flow"

    return app_graph


@phase_name("learn")
async def learn_handler(state: DialogState, persistence: PersistenceLayer) -> dict:
    """
    What you may notice here

    This phase quietly observes what entered the system with the user’s message.

    You may see:
    - newly stated facts,
    - confirmations or rejections,
    - constraints, limits, or choices,
    - small but important details that were not present before.

    Core vector: updating snapshot of the "reality".

    Nothing is interpreted yet.
    Nothing is decided.
    The system simply acknowledges: “Something new is now true.”
    """
    print("- Dialog: Learn")

    response = await exec_prompt(
        prompt_name = "dialog/learn_facts",
        intent = "Analyze request and extract direct or indirect facts from it",
        response_model = LearnFactsResponse,
        request = state.intent
    )

    return {
        "learned_facts": response.learned_facts,
    }

@phase_name("deep")
async def deep_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What becomes visible here

    The system pauses to sense the meaning of the user’s message.

    You may notice:
    - clarification of whether this is a question, an answer, or a command,
    - recognition of curiosity vs. decision vs. execution,
    - early signals of user intent,
    - possible directions this message could be pointing toward.

    Core vector: Understanding before acting.

    This phase asks:
    “What does the user actually intend right now?”
    """
    print("- Dialog: Deep")

    response = await exec_prompt(
        prompt_name = "dialog/deep_classify",
        intent = state.intent,
        response_model = IntentionDescriptor
    )

    return {
        "intention_descriptor": response
    }

@phase_name("connect")
async def connect_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What takes shape here

    The message is placed into the broader landscape of ongoing intentions.

    You may notice:
    - links to earlier topics or paused questions,
    - recognition of continuation, refinement, or branching,
    - emergence of related or parallel intentions,
    - clarification of how this moment fits into the larger journey.

    Core vector: Contextual belonging.

    This phase answers: “What does this connect to?”
    """
    print("- Dialog: Connect")

    return {
    }

@phase_name("service")
async def service_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What happens here

    Decisions become concrete.

    You may notice:
    - a new exploration starting,
    - a clarification process being launched,
    - a concrete action being prepared,
    or, sometimes, a conscious choice to do nothing yet.

    Core vector: Intent becomes structure.

    Here the system decides: “What should be initiated now?”
    """
    print("- Dialog: Service")

    initial_state = SparkState(
        intent = state.intent
    )

    result = await run_graph(
        initial_state = initial_state,
        app_graph = build_spark_graph()
    )

    return {
        "spark": result
    }

@phase_name("knowledge")
async def knowledge_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What becomes clear here

    After action or exploration, the system reflects on what has changed.

    You may notice:
    - new clarity gained,
    - questions that are now resolved,
    - remaining uncertainties becoming visible,
    - stabilization of understanding.

    Core vector: Integration of outcomes.

    This phase gently notes: “This is now known.”
    """
    print("- Dialog: Knowledge")

    spark = state.spark

    content = [SparkContent(content=section, spark_state=spark) for section in spark.content]

    return {
        "content": content
    }

@phase_name("evolution")
async def evolution_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What slowly emerges here

    The system observes patterns across moments, not just within one.

    You may notice:
    - recurring themes,
    - deepening lines of inquiry,
    - shifts in focus,
    - emerging long-term directions.

    Core vector: Trajectory awareness.

    Nothing is enforced.
    The system simply learns how the journey is unfolding.
    """
    print("- Dialog: Evolution")

    return {
    }

@phase_name("responsibility")
async def responsibility_handler(state: DialogState, persistence: PersistenceLayer):
    """
    What closes the loop here

    The system completes its role for this moment.

    You may notice:
    - a brief summary of where things stand,
    - an invitation to respond or adjust,
    - a pause that gives space back to the user,
    - clarity about what happens next.

    Core vector: Shared ownership of the next step.

    This phase says: “Here is where we are. The next move is yours.”
    """
    print("- Dialog: Responsibility")

    return {
    }