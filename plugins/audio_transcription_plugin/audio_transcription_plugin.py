import asyncio
import sounddevice as sd
import numpy as np
import whisper
import os, sys
import logging
from typing import Dict, Any, Optional

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

    def list_audio_devices(self):
        """List available audio devices and recommend input devices."""
        devices = sd.query_devices()
        recommended_devices = []
        for i, device in enumerate(devices):
            self.logger.info(f"Device {i}: {device['name']}")
            # Check for common microphone keywords
            if any(keyword in device['name'].lower() for keyword in ['mic', 'microphone', 'input']):
                recommended_devices.append((i, device['name']))
        
        if recommended_devices:
            self.logger.info("Recommended input devices:")
            for index, name in recommended_devices:
                self.logger.info(f"Device {index}: {name}")
        else:
            self.logger.info("No specific input devices recommended. Please select manually.")
        
        return devices

    async def on_load(self, framer):
        # List and log available audio devices
        devices = self.list_audio_devices()
        # Automatically select the best default device
        recommended_devices = [
            i for i, device in enumerate(devices)
            if any(keyword in device['name'].lower() for keyword in ['mic', 'microphone', 'input'])
        ]
        self.selected_device = recommended_devices[0] if recommended_devices else 0
        self.logger.info(f"Default audio device selected: {devices[self.selected_device]['name']}")
        self.execution_context = framer.execution_context
        self.framer = framer  # Ensure framer is set
        self.action_registry = ActionRegistry(
            execution_context=framer.execution_context
        )
        self.register_actions(self.action_registry)
        self.logger.info("Actions registered in AudioTranscriptionPlugin")
        for action_name in self.action_registry.get_all_actions():
            self.logger.debug(f"Registered action: {action_name}")
        self.logger.info("AudioTranscriptionPlugin loaded")

    async def on_remove(self):
        self.logger.info("AudioTranscriptionPlugin removed")
        # Remove actions from the registry if needed
        self.action_registry.remove_action("record_and_transcribe")
        self.action_registry.remove_action("analyze_transcription")
        self.action_registry.remove_action("continuous_record_and_transcribe")
        self.action_registry.remove_action("understand_intent")

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """
        Execute a specified action with given parameters.

        Args:
            action (str): The action to execute.
            params (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
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
        elif action == "understand_intent":
            transcription = params.get("transcription", "")
            return await self.understand_intent.execute(
                self.execution_context, transcription
            )
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
            max_audio_level = np.max(np.abs(audio))
            logger.debug(f"Max audio level detected: {max_audio_level}")
            try:
                result = self.plugin.model.transcribe(audio, fp16=False)
                logger.info(f"Transcription result: {result}")
            except Exception as e:
                logger.error(f"Error during transcription: {e}")
                result = {"text": ""}
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
            silence_threshold: float = 0.02,
            pause_duration: float = 2.5,
            sample_rate: int = 16000,
            chunk_duration: float = 0.5,
            device: Optional[int] = None,
        ) -> None:
            if device is None:
                device = self.plugin.selected_device
            self.plugin.logger.info(f"Using audio device: {sd.query_devices(device)['name']}")
            if execution_context is None:
                execution_context = self.plugin.execution_context
            logger.info("Starting continuous recording. Press Ctrl+C to stop.")
            silence_duration = 0
            recording = False
            audio_buffer = []

            try:
                while True:
                    audio_chunk = sd.rec(
                        int(chunk_duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype="float32",
                    )
                    sd.wait()
                    audio_chunk = np.squeeze(audio_chunk)
                    max_audio_level = np.max(np.abs(audio_chunk))
                    logger.debug(f"Max audio level detected: {max_audio_level}")

                    if max_audio_level > silence_threshold:
                        recording = True
                        silence_duration = 0
                        audio_buffer.append(audio_chunk)
                    elif recording:
                        silence_duration += chunk_duration
                        if silence_duration >= pause_duration:
                            logger.info("Silence detected, stopping recording.")
                            full_audio = np.concatenate(audio_buffer)
                            transcription = self.plugin.model.transcribe(full_audio, fp16=False)
                            if transcription and "text" in transcription:
                                logger.info(f"Transcription: {transcription['text']}")
                                notes = await self.plugin.analyze_transcription.execute(
                                    execution_context, transcription["text"]
                                )
                                logger.info(f"Actionable Notes: {notes}")
                            else:
                                logger.warning("No transcription text found.")
                            audio_buffer = []
                            recording = False
                    else:
                        audio_buffer = []
                        recording = False
            except KeyboardInterrupt:
                logger.info("Continuous recording stopped.")

    class UnderstandIntentAction(BaseAction):
        def __init__(self, plugin):
            super().__init__(
                "understand_intent",
                "Understand intents from transcription",
                Priority.MEDIUM,
            )
            self.plugin = plugin

        async def execute(
            self, execution_context: ExecutionContext, transcription: str
        ) -> None:
            framer_name = self.plugin.framer.config.name.lower()
            if framer_name in transcription.lower():
                logger.info(f"Framer name '{framer_name}' detected in transcription.")
                # Play a positive sound to acknowledge
                # This is a placeholder for playing sound
                print("Playing positive sound...")
                # Start listening to the user
                print("Framer is now listening to the user...")

    def register_actions(self, action_registry):
        self.understand_intent = self.UnderstandIntentAction(self)
        self.record_and_transcribe = self.RecordAndTranscribeAction(self)
        self.analyze_transcription = self.AnalyzeTranscriptionAction()
        self.continuous_record_and_transcribe = (
            self.ContinuousRecordAndTranscribeAction(self)
        )

        self.logger.debug("Registering actions in AudioTranscriptionPlugin")
        action_registry.add_action(
            self.record_and_transcribe,
        )
        self.logger.debug("Registered action: record_and_transcribe")
        action_registry.add_action(
            self.analyze_transcription,
        )
        self.logger.debug("Registered action: analyze_transcription")
        action_registry.add_action(
            self.continuous_record_and_transcribe,
        )
        self.logger.debug("Registered action: continuous_record_and_transcribe")
        action_registry.add_action(
            self.understand_intent,
        )
        self.logger.debug("Registered action: understand_intent")
