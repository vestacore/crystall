
from exec_prompt import exec_prompt
from units.project_intent.models import IntentionProjection

async def project_intent(intent: str)->IntentionProjection:

    response = await exec_prompt(
        prompt_name = "project_intent/prompt",
        intent = intent,
        response_model = IntentionProjection
    )

    return response
