import os
import asyncio
import argparse
from frame import Frame
from examples.framer_created_from_json.main import export_config, import_config


async def main(action, filename):
    frame = Frame()

    if action == "export":
        await export_config(frame, filename)
    elif action == "import":
        framer = await import_config(filename)
        print(f"Imported Framer configuration: {framer.__dict__}")
    else:
        print("Invalid action. Use 'export' or 'import'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI for exporting and importing Framer configurations."
    )
    parser.add_argument(
        "action",
        choices=["export", "import"],
        help="Action to perform: export or import",
    )
    parser.add_argument("filename", help="Filename for the configuration")

    args = parser.parse_args()
    asyncio.run(main(args.action, args.filename))
