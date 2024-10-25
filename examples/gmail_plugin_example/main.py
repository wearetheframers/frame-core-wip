import asyncio
import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from plugins.gmail_plugin.gmail_plugin import GmailPlugin


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the GmailPlugin
    config = FramerConfig(name="GmailFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the GmailPlugin
    # Define the path to the token file
    token_file_path = os.path.join(os.path.dirname(__file__), "credentials.json")
    print("Token file path:", token_file_path)

    # Initialize the GmailPlugin with the token file path
    gmail_plugin = GmailPlugin(framer)
    await gmail_plugin.on_load(framer)
    framer.plugins["gmail_plugin"] = gmail_plugin

    # Read emails
    execution_context = {}  # Define the execution context as needed
    response = await framer.use_plugin_action(
        "gmail_plugin", "read_emails", {"execution_context": execution_context}
    )
    print(f"Email reading response: {response}")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
