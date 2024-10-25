import asyncio
import os, sys
# Add the project root to the Python path to ensure all modules can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from gmail_plugin import GmailPlugin

async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the GmailPlugin
    config = FramerConfig(name="GmailFramer", default_model="gpt-4o-mini")
    framer = await frame.create_framer(config)

    # Register the GmailPlugin
    gmail_plugin = GmailPlugin(framer)
    framer.plugins["gmail_plugin"] = gmail_plugin

    # Read emails
    response = await framer.use_plugin_action("gmail_plugin", "read_emails", {})
    print(f"Email reading response: {response}")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
