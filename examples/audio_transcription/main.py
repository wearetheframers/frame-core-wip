import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from plugins.audio_transcription_plugin import AudioTranscriptionPlugin


async def main():
    frame = Frame()
    config = FramerConfig(
        name="AudioTranscriptionFramer", default_model="gpt-3.5-turbo"
    )
    framer = await frame.create_framer(config=config)

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

    # Update the agency, brain, and execution context with the new roles and goals
    framer.agency.set_roles(roles)
    framer.agency.set_goals(goals)
    framer.execution_context.set_roles(roles)
    framer.execution_context.set_goals(goals)
    framer.execution_context.set_roles(roles)
    framer.execution_context.set_goals(goals)

    # Initialize and load the AudioTranscriptionPlugin
    at_plugin = AudioTranscriptionPlugin()
    await at_plugin.on_load(framer)

    # Register actions with the main action registry of the Framer
    at_plugin.register_actions(framer.brain.action_registry)

    # List available audio devices
    devices = at_plugin.list_audio_devices()
    print("Available audio devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']}")
    device_choice = input(
        f"Select audio device by number (default is {at_plugin.selected_device}): "
    )
    try:
        selected_device = int(device_choice)
    except ValueError:
        selected_device = 0
    if 0 <= selected_device < len(devices):
        at_plugin.selected_device = selected_device
    else:
        print(
            f"Invalid selection. Using default device: {devices[at_plugin.selected_device]['name']}"
        )
    try:
        print("1. Singular Recording")
        print("2. Continuous Live Recording")
        choice = input("Enter choice (1 or 2): ")

        if choice == "1":
            print("\nRecording audio... (Press Ctrl+C to stop)")
            transcription = await framer.brain.action_registry.execute_action(
                "record_and_transcribe"
            )
            print(f"Transcription: {transcription}")

            notes = await framer.brain.action_registry.execute_action(
                "analyze_transcription", transcription=transcription
            )
            print(f"Actionable Notes: {notes}")

        elif choice == "2":
            print("\nStarting continuous live recording... (Press Ctrl+C to stop)")
            await framer.brain.action_registry.execute_action(
                "continuous_record_and_transcribe"
            )

        else:
            print("Invalid choice. Please restart and select 1 or 2.")
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")

    await framer.close()


if __name__ == "__main__":
    asyncio.run(main())
