import asyncio
import sounddevice as sd
import numpy as np
import whisper
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.src.framer.agency.actions import BaseAction
from frame.src.services.execution_context import ExecutionContext
from frame.src.framer.agency.priority import Priority


class AudioTranscriptionPlugin:
    def __init__(self):
        self.model = whisper.load_model("base")

    class RecordAndTranscribeAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "record_and_transcribe", "Record and transcribe audio", Priority.HIGH
            )
            self.plugin = plugin

        async def execute(self, execution_context: ExecutionContext) -> str:
            duration = 5  # seconds
            sample_rate = 16000  # Hz

            print("Recording...")
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="float32",
            )
            sd.wait()
            print("Recording finished.")

            audio = np.squeeze(audio)
            result = self.plugin.model.transcribe(audio, fp16=False)
            print(f"Transcription result: {result}")
            return result["text"]

    class AnalyzeTranscriptionAction(BaseAction):
        def __init__(self):
            super().__init__(
                "analyze_transcription",
                "Analyze transcription and create notes",
                Priority.MEDIUM,
            )

        async def execute(
            self, execution_context: ExecutionContext, transcription: str
        ) -> str:
            notes = f"Analyzed notes from transcription: {transcription}"
            print(f"{execution_context.framer.config.name}: Analysis completed")
            return notes

    class ContinuousRecordAndTranscribeAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "continuous_record_and_transcribe",
                "Continuously record and transcribe audio",
                Priority.HIGH,
            )
            self.plugin = plugin

        async def execute(self, execution_context: ExecutionContext) -> None:
            print("Starting continuous recording. Press Ctrl+C to stop.")
            try:
                while True:
                    transcription = await self.plugin.record_and_transcribe.execute(
                        execution_context
                    )
                    if transcription:
                        print(f"Transcription: {transcription}")
                        notes = await self.plugin.analyze_transcription.execute(
                            execution_context, transcription
                        )
                        print(f"Actionable Notes: {notes}")
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Continuous recording stopped.")

    def register_actions(self, action_registry):
        self.record_and_transcribe = self.RecordAndTranscribeAction(self)
        self.analyze_transcription = self.AnalyzeTranscriptionAction()
        self.continuous_record_and_transcribe = (
            self.ContinuousRecordAndTranscribeAction(self)
        )

        action_registry.register_action(self.record_and_transcribe)
        action_registry.register_action(self.analyze_transcription)
        action_registry.register_action(self.continuous_record_and_transcribe)
