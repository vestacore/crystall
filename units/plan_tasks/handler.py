
from exec_prompt import exec_prompt

from units.project_intent.models import IntentionProjection
from units.plan_tasks.models import ProcessPlannerResponse

async def plan_tasks(intent: str, intent_projection: IntentionProjection) -> ProcessPlannerResponse:

    response = await exec_prompt(
        prompt_name = "plan_tasks/prompt",
        intent = intent,
        response_model = ProcessPlannerResponse,
        intent_projection = intent_projection
    )

    return response
