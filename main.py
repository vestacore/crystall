import asyncio
from dotenv import load_dotenv

from dialog.run import run_dialog

load_dotenv()

if __name__ == "__main__":

    try:

        request = "I want to understand the structure of EU DORA regulation as it applies to the work of European payment service providers."

        asyncio.run(run_dialog(request))

    except Exception as e:
        print(f"\n[!] Execution Failed: {e}")
        import traceback

        traceback.print_exc()

