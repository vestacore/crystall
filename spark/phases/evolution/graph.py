from langgraph.constants import END
from langgraph.graph import StateGraph

from spark.state import SparkState


def build_evolution_graph():
    """
    Purpose:
    The Evolution phase transforms the outcome of the interaction into a lasting, directional layer of understanding.
    It integrates insights, clarifies emerging tendencies, and forms gentle vectors of future development without
    prescribing any specific path.

    - Synthesis of Meaning
      The system distills the essential insight of the completed interaction, identifying patterns, resonances,
      and shifts in the user's conceptual field.

    - Formation of Evolution Vectors
      Key directions that naturally emerge from the user’s intention and the interaction are articulated as open,
      non-directive potentials — possibilities the user may explore if they choose.

    - Integration into Long-Term Context
      The interaction’s distilled meaning is converted into a compact evolution artifact (e.g., semantic tags,
      micro-intent vectors, thematic threads), enabling future phases to understand where the user is moving.

    - Support for Continued Growth
      The system highlights opportunities for deepening, clarification, or expansion — always as invitations,
      never as requirements.
      Agency and responsibility remain fully with the user.

    - Preparation for the Next Cycle
      Evolution outputs a structured but lightweight layer of context that will inform future Understand and
      Service phases, supporting continuity, coherence, and resonance across iterations.

    Role in the Spiral:
    Evolution closes the current cycle while simultaneously opening the next one.
    It transforms a single interaction from an isolated event into part of a broader journey, enabling the system and the user to move through the spiral with increasing clarity, integration, and intention.
    """
    workflow = StateGraph(SparkState)

    workflow.add_node("reflections", reflections_handler)

    workflow.set_entry_point("reflections")
    workflow.add_edge("reflections", END)

    app_graph = workflow.compile()
    app_graph.name = "spiral_evolution_flow"

    return app_graph


async def reflections_handler(state: SparkState):
    print("- Evolution:Reflections")

    return {
    }
