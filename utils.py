import typing

from dialog.state import DialogState
from spark.phases.understand.cunit.state import CUnitState
from spark.phases.service.funits.llm.state import LLMExecState
from spark.phases.connect.punit.state import PUnitState
from spark.state import SparkState

T = typing.TypeVar("T", bound=typing.Union[CUnitState, PUnitState, LLMExecState, SparkState, DialogState])

async def run_graph(initial_state: T, app_graph) -> T:

    result = await app_graph.ainvoke(initial_state)
    if isinstance(result, dict):
        state_cls = type(initial_state)
        result = state_cls.model_validate(result)

    return result
