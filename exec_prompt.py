import typing

import jinja2
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from pydantic import BaseModel

import instructor
from openai import AsyncOpenAI
from langsmith.wrappers import wrap_openai

# 1. Настройка окружения шаблонов
template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("units")
)

raw_client = AsyncOpenAI()
# Link OpenAI calls with LangGraph tracing
client = instructor.from_openai(wrap_openai(raw_client))

def get_prompt(name: str, *args: typing.Any, **kwargs: typing.Any):
    template = template_env.get_template(f"{name}.j2")
    return template.render(*args, **kwargs)

T = typing.TypeVar("T", bound=typing.Union[BaseModel, "Iterable[Any]", "Partial[Any]"])

async def exec_prompt(prompt_name: str, intent: str, response_model: type[T], *args: typing.Any, **kwargs: typing.Any) -> T:

    system_prompt = get_prompt(prompt_name, *args, **kwargs)
    user_prompt = intent

    response = await client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt)
        ],
        response_model=response_model
    )

    return response
