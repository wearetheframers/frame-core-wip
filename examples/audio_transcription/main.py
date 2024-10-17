import sys
import os
import asyncio
from frame import Frame, FramerConfig
from audio_transcription_plugin import AudioTranscriptionPlugin

async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize configuration
    config = FramerConfig(name="AudioTranscriptionFramer")

    # Create a Framer instance
    framer = await frame.create_framer(config)

    # Initialize the Framer
    await framer.initialize()

    # Initialize and register the plugin
    at_plugin = AudioTranscriptionPlugin()
    framer.brain.action_registry.add_action("transcribe_audio", at_plugin.transcribe_audio)
    framer.brain.action_registry.add_action("analyze_transcription", at_plugin.analyze_transcription)

    # Simulate audio input
    print("\nRecording audio... (Press Ctrl+C to stop)")
    transcription = await at_plugin.record_and_transcribe_audio()
    print(f"Transcription: {transcription}")

    # Analyze transcription
    notes = await framer.sense({"type": "audio", "data": {"transcription": transcription}})
    print(f"Actionable Notes: {notes}")

    # Clean up
    await framer.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
