
from exec_prompt import exec_prompt
from units.deep_classify.models import IntentionDescriptor


async def deep_classify(intent: str)->IntentionDescriptor:

    response = await exec_prompt(
        prompt_name = "deep_classify/prompt",
        intent = intent,
        response_model = IntentionDescriptor
    )

    return response

