import asyncio
import multiprocessing
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

    def __init__(
        self,
        config=None,
        base_sound_level: int = 50,
        sensitivity: int = 50,
        should_setup_mic: bool = True,
        should_setup_mic_loop: bool = True,
        setup_interval: int = 6000,
    ):
        """
        Initialize the AudioTranscriptionPlugin.

        Args:
            config (Optional[Dict[str, Any]]): Configuration for the plugin.
            base_sound_level (int): The base sound level of the environment (0-100).
            sensitivity (int): The sensitivity level for sound detection (0-100).
            should_setup_mic (bool): Whether to set up the microphone initially.
            should_setup_mic_loop (bool): Whether to continuously recheck sensitivity levels.
        """
        super().__init__(framer=None)  # Ensure BasePlugin's init is called
        self.logger = logging.getLogger(self.__class__.__name__)
        self.action_registry = None
        self.base_sound_level = base_sound_level
        self.sensitivity = sensitivity
        self.model = whisper.load_model("base")
        self.framer = None  # Initialize framer attribute
        self.should_setup_mic = should_setup_mic
        self.selected_device = 0  # Initialize selected_device with a default value
        self.should_setup_mic_loop = should_setup_mic_loop

        self.adjust_sensitivity_duration_check = 5
        self.setup_interval = (
            60  # Interval in seconds for rechecking sensitivity levels
        )

    async def on_load(self, framer):
        self.framer = framer
        self.logger.info("AudioTranscriptionPlugin loaded")
        if self.should_setup_mic:
            await self.setup_microphone(self.framer)

    def adjust_sensitivity(self):
        print("Setting up microphone for background noise analysis.")
        self.logger.info("Setting up microphone for background noise analysis.")
        duration = self.adjust_sensitivity_duration_check  # seconds
        sample_rate = 16000
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        audio = np.squeeze(audio)
        average_level = np.mean(np.abs(audio))
        self.logger.info(f"Average background noise level: {average_level}")
        print(f"Average background noise level: {average_level}")
        # Map audio levels to sensitivity
        # Adjust the sensitivity calculation to be more responsive to changes in noise level
        raw_sensitivity = max(0, min(100, (1 - average_level) * 1000))
        self.sensitivity = max(10, min(100, int(raw_sensitivity)))
        self.logger.info(f"Mapped sensitivity: {self.sensitivity}")
        print(f"Sensitivity adjusted to: {self.sensitivity}")
        # List and log available audio devices
        devices = self.list_audio_devices()
        # # Automatically select the best default device
        recommended_devices = [
            i
            for i, device in enumerate(devices)
            if any(
                keyword in device["name"].lower()
                for keyword in ["mic", "microphone", "input"]
            )
        ]
        # self.selected_device = recommended_devices[0] if recommended_devices else 0
        self.selected_device[0]
        self.logger.info(
            f"Default audio device selected: {devices[self.selected_device]['name']}"
        )
        print("Default audio device selected: {devices[self.selected_device]['name']}")
        print("Finished setting up microphone.")

    async def setup_microphone(self, framer):
        """
        Record for 10 seconds to listen for background noise, calculate an average sound level,
        and adjust the sensitivity based on this average.
        """
        while self.should_setup_mic_loop:
            # Run the sensitivity adjustment in a separate process
            process = multiprocessing.Process(
                target=self.adjust_sensitivity, args=(self.base_sound_level,)
            )
            process.start()
            # Do not join the process to allow non-blocking behavior

            if not self.should_setup_mic_loop:
                break

            # Optionally, set a flag or use a callback to handle completion

    @staticmethod
    def adjust_sensitivity(base_sound_level):
        print("Setting up microphone for background noise analysis.")
        logger = logging.getLogger("AudioTranscriptionPlugin")
        logger.info("Setting up microphone for background noise analysis.")
        duration = 10  # seconds
        sample_rate = 16000
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        audio = np.squeeze(audio)
        average_level = np.mean(np.abs(audio))
        logger.info(f"Average background noise level: {average_level}")
        print(f"Average background noise level: {average_level}")
        # Map audio levels to sensitivity
        # Use a logarithmic scale to map average_level (0 to 1) to sensitivity (10 to 100)
        # This ensures that small changes in noise level have a larger impact on sensitivity
        # while larger changes have a diminishing effect.
        # Use a more aggressive mapping to adjust sensitivity
        # Invert the sensitivity calculation to increase sensitivity with higher noise levels
        sensitivity = 10 + (np.log1p(average_level * 1000) * 90)
        sensitivity = max(10, min(100, int(sensitivity)))
        logger.info(f"Mapped sensitivity: {sensitivity}")
        print("Sensitivity adjusted to:", sensitivity)
        # List and log available audio devices
        devices = sd.query_devices()
        # Automatically select the best default device
        recommended_devices = [
            i
            for i, device in enumerate(devices)
            if any(
                keyword in device["name"].lower()
                for keyword in ["mic", "microphone", "input"]
            )
        ]
        selected_device = recommended_devices[0] if recommended_devices else 0
        logger.info(
            f"Default audio device selected: {devices[selected_device]['name']}"
        )
        print(f"Default audio device selected: {devices[selected_device]['name']}")
        print("Finished setting up microphone.")

    def list_audio_devices(self):
        """
        List available audio devices and recommend input devices.
        """
        devices = sd.query_devices()
        recommended_devices = []
        for i, device in enumerate(devices):
            # Check for common microphone keywords
            if any(
                keyword in device["name"].lower()
                for keyword in ["mic", "microphone", "input"]
            ):
                recommended_devices.append((i, device["name"]))
        self.logger.info(f"Recommended audio devices: {recommended_devices}")
        return devices

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

        The silence threshold and sound detection are adjusted based on the base sound level and sensitivity.

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
            self.logger.info("Executing continuous_record_and_transcribe action.")
            return await self.continuous_record_and_transcribe.execute(
                self.execution_context
            )
        elif action == "understand_intent":
            transcription = params.get("transcription", "")
            return await self.understand_intent.execute(
                self.execution_context, transcription
            )

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
            print("WE FLUFFIN")
            super().__init__(
                "continuous_record_and_transcribe",
                "Continuously record and transcribe audio",
                Priority.HIGH,
            )
            self.plugin = plugin

        async def execute(
            self,
            execution_context: ExecutionContext = None,
            pause_duration: float = 2.5,
            sample_rate: int = 16000,
            chunk_duration: float = 0.5,
            device: Optional[int] = None,
        ) -> None:
            print("WE FLUFFIN2")
            silence_threshold: float = 0.02 * (1 - self.plugin.base_sound_level / 100)
            print("WE FLUFFIN3")
            if device is None:
                device = self.plugin.selected_device
            print(f"Using audio device: {sd.query_devices(device)['name']}")
            print(
                f"Base sound level: {self.plugin.base_sound_level}, Sensitivity: {self.plugin.sensitivity}"
            )
            print("Starting continuous recording. Press Ctrl+C to stop.")
            print(
                "Adjusting silence threshold and sound detection based on base sound level and sensitivity."
            )
            if execution_context is None:
                execution_context = self.plugin.execution_context
            print("Starting continuous recording. Press Ctrl+C to stop.")
            silence_duration = 0
            recording = False
            audio_buffer = []

            try:
                while True:
                    logger.debug("Recording audio chunk...")
                    audio_chunk = sd.rec(
                        int(chunk_duration * sample_rate),
                        samplerate=sample_rate,
                        channels=1,
                        dtype="float32",
                    )
                    sd.wait()
                    logger.debug("Audio chunk recorded.")
                    # print("Audio chunk recorded.")
                    audio_chunk = np.squeeze(audio_chunk)
                    logger.debug(f"Audio chunk shape: {audio_chunk.shape}")
                    # print(f"Audio chunk shape: {audio_chunk.shape}")
                    max_audio_level = np.max(np.abs(audio_chunk))
                    logger.debug(f"Max audio level detected: {max_audio_level}")
                    # print(f"Max audio level detected: {max_audio_level}")
                    if max_audio_level > silence_threshold * (
                        self.plugin.sensitivity / 50
                    ):
                        if not recording:
                            print("Sound detected, starting recording.")
                            logger.info("Sound detected, starting recording.")
                        silence_duration = 0
                        audio_buffer.append(audio_chunk)
                    elif recording:
                        silence_duration += chunk_duration
                        if silence_duration >= pause_duration:
                            print("Silence detected, stopping recording.")
                            full_audio = np.concatenate(audio_buffer)
                            print("Transcribing audio...")
                            transcription = self.plugin.model.transcribe(
                                full_audio, fp16=False
                            )
                            if transcription and "text" in transcription:
                                logger.info(f"Transcription: {transcription['text']}")
                                notes = await self.plugin.analyze_transcription.execute(
                                    execution_context, transcription["text"]
                                )
                                print(f"Actionable Notes: {notes}")
                            else:
                                print("No transcription text found.")
                                logger.warning("No transcription text found.")
                            audio_buffer = []
                            recording = False
                    else:
                        audio_buffer = []
                        recording = False
            except KeyboardInterrupt:
                print("Continuous recording stopped.")
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
