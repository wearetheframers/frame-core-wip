import asyncio
import sounddevice as sd
import numpy as np
import whisper
import os, sys
import logging
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

logger = logging.getLogger(__name__)

from frame.src.framer.brain.actions import BaseAction
from frame.src.framer.brain.action_registry import ActionRegistry
from frame.src.services import ExecutionContext
from frame.src.framer.agency.priority import Priority


from frame.src.framer.brain.plugins.base import BasePlugin


class AudioTranscriptionPlugin(BasePlugin):
    def __init__(self, config=None):
        super().__init__(framer=None)  # Ensure BasePlugin's init is called
        self.logger = logging.getLogger(self.__class__.__name__)
        self.action_registry = None
        self.model = whisper.load_model("base")

    async def on_load(self, framer):
        self.execution_context = framer.execution_context
        self.framer = framer  # Ensure framer is set
        self.action_registry = ActionRegistry(
            execution_context=framer.execution_context
        )
        self.register_actions(self.action_registry)
        self.logger.info("AudioTranscriptionPlugin loaded")

    async def on_remove(self):
        self.logger.info("AudioTranscriptionPlugin removed")
        # Remove actions from the registry if needed
        self.action_registry.remove_action("record_and_transcribe")
        self.action_registry.remove_action("analyze_transcription")
        self.action_registry.remove_action("continuous_record_and_transcribe")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "record_and_transcribe":
            return await self.record_and_transcribe.execute(self.execution_context)
        elif action == "analyze_transcription":
            transcription = params.get("transcription", "")
            return await self.analyze_transcription.execute(
                self.execution_context, transcription
            )
        elif action == "continuous_record_and_transcribe":
            return await self.continuous_record_and_transcribe.execute(
                self.execution_context
            )
        else:
            raise ValueError(f"Unknown action: {action}")

    class RecordAndTranscribeAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "record_and_transcribe", "Record and transcribe audio", Priority.HIGH
            )
            self.plugin = plugin

        async def execute(
            self,
            execution_context: ExecutionContext,
            duration: int = 5,
            sample_rate: int = 16000,
        ) -> str:

            logger.debug("Recording...")
            audio = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="float32",
            )
            sd.wait()
            logger.debug("Recording finished.")

            audio = np.squeeze(audio)
            result = self.plugin.model.transcribe(audio, fp16=False)
            logger.info(f"Transcription result: {result}")
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
            notes = f"Transcription: {transcription}"
            if hasattr(execution_context, "framer"):
                logger.info(
                    f"{execution_context.framer.config.name}: Analysis completed"
                )
            else:
                if hasattr(execution_context, "framer"):
                    logger.info(
                        f"{execution_context.framer.config.name}: Analysis completed"
                    )
            return notes

    class ContinuousRecordAndTranscribeAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "continuous_record_and_transcribe",
                "Continuously record and transcribe audio",
                Priority.HIGH,
            )
            self.plugin = plugin

        async def execute(
            self,
            execution_context: ExecutionContext = None,
            pause_threshold: float = 3.0,
        ) -> None:
            if execution_context is None:
                execution_context = self.plugin.execution_context
            logger.info("Starting continuous recording. Press Ctrl+C to stop.")
            pause_threshold = pause_threshold  # seconds
            silence_duration = 0  # Initialize silence duration
            try:
                while True:
                    audio = sd.rec(
                        int(10 * 16000), samplerate=16000, channels=1, dtype="float32"
                    )
                    sd.wait()
                    audio = np.squeeze(audio)
                    logger.debug("Recording...")
                    logger.debug(f"Audio data: {audio}")

                    # Check for pause
                    if np.max(np.abs(audio)) < 0.02:  # Adjust threshold as needed
                        silence_duration += (
                            10  # Increment silence duration by 10 seconds
                        )
                        if silence_duration >= pause_threshold:
                            logger.info(
                                "Silence detected for 3 seconds, stopping recording."
                            )
                            break
                    else:
                        silence_duration = (
                            0  # Reset silence duration if speech is detected
                        )
                        transcription = self.plugin.model.transcribe(audio, fp16=False)
                        if transcription and "text" in transcription:
                            logger.info(f"Transcription: {transcription['text']}")
                            notes = await self.plugin.analyze_transcription.execute(
                                execution_context, transcription["text"]
                            )
                            logger.info(f"Actionable Notes: {notes}")
                        else:
                            logger.warning("No transcription text found.")
            except KeyboardInterrupt:
                logger.info("Continuous recording stopped.")

    def register_actions(self, action_registry):
        self.record_and_transcribe = self.RecordAndTranscribeAction(self)
        self.analyze_transcription = self.AnalyzeTranscriptionAction()
        self.continuous_record_and_transcribe = (
            self.ContinuousRecordAndTranscribeAction(self)
        )

        action_registry.add_action(self.record_and_transcribe)
        action_registry.add_action(self.analyze_transcription)
        action_registry.add_action(self.continuous_record_and_transcribe)
