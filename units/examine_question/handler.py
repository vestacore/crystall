
from exec_prompt import exec_prompt

from units.project_intent.models import IntentionProjection
from units.examine_question.models import LLMExecutorResponse

async def examine_question(initial_intent: str, 
                           intent_projection: IntentionProjection, 
                           question: str)->LLMExecutorResponse:

    response = await exec_prompt(
        prompt_name = "examine_question/prompt",
        intent = question,
        response_model = LLMExecutorResponse,
        initial_intent = initial_intent,
        intent_projection = intent_projection
    )

    return response
