

from exec_prompt import exec_prompt
from units.project_intent.models import IntentionProjection
from units.extract_concepts.models import Concepts
from units.extract_concepts.models import Concept

async def extract_concepts(intent: str, projection: IntentionProjection)->list[Concept]:

    response = await exec_prompt(
        prompt_name = "extract_concepts/prompt",
        intent = intent,
        response_model = Concepts,
        intent_projection = projection
    )

    return response.concepts
