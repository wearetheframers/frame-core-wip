import asyncio
import os
import sys

# Add the project root to the Python path to ensure all modules can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from plugins.audio_transcription_plugin.audio_transcription_plugin import (
    AudioTranscriptionPlugin,
)


async def main():
    # Initialize Frame
    frame = Frame()

    # Create a Framer instance with the necessary permissions
    config = FramerConfig(
        name="Framer",
        default_model="gpt-3.5-turbo",
        permissions=["with_memory", "with_shared_context"],
    )
    framer = await frame.create_framer(config)

    # Initialize and load the audio transcription plugin
    audio_plugin = AudioTranscriptionPlugin()
    await audio_plugin.on_load(framer=framer)
    framer.add_plugin("audio_transcription", audio_plugin)

    try:
        while True:
            # Simulate continuous listening
            print("Framer is listening for its name...")
            await asyncio.sleep(1)  # Simulate a delay between checks
    except KeyboardInterrupt:
        print("Stopping the Framer...")
    finally:
        await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
