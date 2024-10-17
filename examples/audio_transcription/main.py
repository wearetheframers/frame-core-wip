import sys
import os
import asyncio

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig
from audio_transcription_plugin import AudioTranscriptionPlugin


async def main():
    # Initialize the Frame
    frame = Frame()

    # Initialize configuration
    config = FramerConfig(name="AudioTranscriptionFramer")

    # Define roles and goals
    roles = [
        {
            "name": "Listener",
            "description": "Listens to audio input and transcribes it.",
        },
        {
            "name": "Analyzer",
            "description": "Analyzes transcriptions to create actionable notes.",
        },
    ]
    goals = [
        {
            "name": "Transcribe Audio",
            "description": "Accurately transcribe audio input.",
        },
        {
            "name": "Generate Notes",
            "description": "Create detailed notes from transcriptions.",
        },
    ]

    # Create a Framer instance
    framer = await frame.create_framer(config)

    # Initialize the Framer with roles and goals
    await framer.initialize()

    at_plugin = AudioTranscriptionPlugin()
    framer.brain.action_registry.add_action(
        "transcribe_audio", at_plugin.transcribe_audio
    )
    framer.brain.action_registry.add_action(
        "analyze_transcription", at_plugin.analyze_transcription
    )

    print("Select mode:")
    print("1. Singular Recording")
    print("2. Continuous Live Recording")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        # Singular recording
        print("\nRecording audio... (Press Ctrl+C to stop)")
        transcription = await at_plugin.record_and_transcribe_audio()
        print(f"Transcription: {transcription}")

        # Analyze transcription
        notes = await at_plugin.analyze_transcription(framer, transcription)
        print(f"Actionable Notes: {notes}")

    elif choice == "2":
        # Continuous live recording
        await at_plugin.continuous_record_and_transcribe(framer)

    else:
        print("Invalid choice. Please restart and select 1 or 2.")

    # Clean up
    await framer.close()


# Run the example
if __name__ == "__main__":
    asyncio.run(main())
