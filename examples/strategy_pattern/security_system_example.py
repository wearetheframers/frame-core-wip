import asyncio
import os
import sounddevice as sd
import numpy as np
import sys
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Add the project root to the Python path to ensure all modules can be imported correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame import Frame, FramerConfig
from plugins.audio_transcription_plugin.audio_transcription_plugin import (
    AudioTranscriptionPlugin,
)


class AdaptiveSecurityPlugin:
    def __init__(self, framer):
        self.framer = framer
        self.audio_plugin = AudioTranscriptionPlugin()
        self.security_level = 5  # Default security level

    async def on_load(self):
        await self.audio_plugin.on_load(framer=self.framer)
        self.framer.add_plugin("audio_transcription", self.audio_plugin)

    async def evaluate_security(self, context, tolerance_level):
        current_time = datetime.now().hour
        if context.get("security_level", self.security_level) > int(
            tolerance_level
        ) or current_time in range(22, 6):
            logging.debug(
                f"Security evaluation at {datetime.now()}: High risk detected."
            )
            print("High security risk detected. Activating sound recording.")
            await self.monitor_audio(int(tolerance_level))
        else:
            print("Security level is normal. No action required.")

    async def monitor_audio(self, tolerance_level):
        logging.debug(f"Audio monitoring started at {datetime.now()}.")
        threshold_db = (
            60 + (10 - tolerance_level) * 2
        )  # Example calculation for threshold
        try:
            while True:
                audio = sd.rec(
                    int(1 * 16000), samplerate=16000, channels=1, dtype="float32"
                )
                sd.wait()
                audio = np.squeeze(audio)
                volume_norm = np.linalg.norm(audio) * 10
                if volume_norm > threshold_db:
                    logging.debug(
                        f"High volume detected at {datetime.now()}: {volume_norm} dB. Activating security measures."
                    )
                    await self.audio_plugin.execute(
                        "continuous_record_and_transcribe", {}
                    )
                await asyncio.sleep(1)  # Check every second
        except KeyboardInterrupt:
            print("Audio monitoring stopped.")


async def main():
    logger.info("Initializing Security System...")
    try:
        # Initialize Frame
        frame = Frame()

        # Create a Framer instance with the necessary permissions
        config = FramerConfig(
            name="Security Framer",
            default_model="gpt-3.5-turbo",
            permissions=["with_memory", "with_shared_context"],
        )
        framer = await frame.create_framer(config)

        # Initialize and load the security plugin
        security_plugin = AdaptiveSecurityPlugin(framer)
        await security_plugin.on_load()

        # Define a context for security evaluation
        context = {"security_level": 7}  # Example context with high security level
        while True:
            tolerance_level = input(
                "Set the security tolerance level (1-10) or type 'quit' to exit: "
            )
            if tolerance_level.lower() == "quit":
                logger.info("Shutting down Security System...")
                break
            await security_plugin.evaluate_security(context, tolerance_level)
            await asyncio.sleep(1)  # Add a small delay to prevent rapid looping

    finally:
        await framer.close()
        logger.info("Security System has been shut down.")


if __name__ == "__main__":
    asyncio.run(main())
