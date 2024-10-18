import sys
import os
import asyncio
from frame import Frame, FramerConfig
from audio_transcription_plugin import AudioTranscriptionPlugin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

async def main():
    frame = Frame()
    config = FramerConfig(name="AudioTranscriptionFramer")
    framer = await frame.create_framer(config)

    roles = [
        {"name": "Listener", "description": "Listens to audio input and transcribes it."},
        {"name": "Analyzer", "description": "Analyzes transcriptions to create actionable notes."},
    ]
    goals = [
        {"name": "Transcribe Audio", "description": "Accurately transcribe audio input."},
        {"name": "Generate Notes", "description": "Create detailed notes from transcriptions."},
    ]

    await framer.initialize(roles=roles, goals=goals)

    at_plugin = AudioTranscriptionPlugin()
    at_plugin.register_actions(framer.brain.action_registry)

    print("Select mode:")
    print("1. Singular Recording")
    print("2. Continuous Live Recording")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        print("\nRecording audio... (Press Ctrl+C to stop)")
        transcription = await framer.brain.action_registry.execute_action("record_and_transcribe")
        print(f"Transc ription: {transcription}")

        notes = await framer.brain.action_registry.execute_action("analyze_transcription", {"transcription": transcription})
        print(f"Actionable Notes: {notes}")

    elif choice == "2":
        await framer.brain.action_registry.execute_action("continuous_record_and_transcribe")

    else:
        print("Invalid choice. Please restart and select 1 or 2.")

    await framer.close()

if __name__ == "__main__":
    asyncio.run(main())
