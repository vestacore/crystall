from dialog.graph import build_dialog_graph, learn_handler, deep_handler, connect_handler, service_handler, \
    knowledge_handler, evolution_handler, responsibility_handler
from dialog.state import DialogState, dialog_save_state
from persistence.file_persistence import FilePersistence
from utils import run_graph


async def run_dialog(intent: str)-> DialogState:

    print("Running dialog...")

    persistence = FilePersistence("1")

    initial_state = DialogState(
         intent=intent
    )

    # initial_state = dialog_load_state("1")

    result = await run_graph(
        initial_state = initial_state,
        app_graph = build_dialog_graph(
            phase_handlers = [
                learn_handler,
                deep_handler,
                connect_handler,
                service_handler,
                knowledge_handler,
                evolution_handler,
                responsibility_handler
            ],
            persistence=persistence
        )
    )

    dialog_save_state(result, "4")

    return result
