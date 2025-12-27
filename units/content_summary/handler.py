
from exec_prompt import exec_prompt

from units.project_intent.models import IntentionProjection
from units.examine_question.models import ContentSection
from units.content_summary.models import ContentSummary

async def content_summary(initial_intent: str, 
                          intent_projection: IntentionProjection,
                          content: list[ContentSection])->ContentSummary:

    response = await exec_prompt(
        prompt_name = "content_summary/prompt",
        intent = initial_intent,
        response_model= ContentSummary,
        intent_projection = intent_projection,
        content = content
    )

    return response