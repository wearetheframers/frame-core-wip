import asyncio
import sounddevice as sd
import numpy as np
import whisper


class AudioTranscriptionPlugin:

    def __init__(self):
        # Initialize any necessary state or resources
        self.model = whisper.load_model("base")

    async def record_and_transcribe_audio(self):
        # Record audio for a fixed duration
        duration = 5  # seconds
        sample_rate = 16000  # Hz

        print("Recording...")
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")

        # Convert audio to numpy array and transcribe
        audio = np.squeeze(audio)
        result = self.model.transcribe(audio, fp16=False)
        print(f"Transcription result: {result}")
        return result["text"]

    async def transcribe_audio(self, execution_context):
        transcription = await self.record_and_transcribe_audio()
        print(f"{execution_context.framer.config.name}: Transcription completed")
        return transcription

    async def analyze_transcription(self, framer, transcription: str):
        # Simulate analysis of transcription
        notes = f"Analyzed notes from transcription: {transcription}"
        print(f"{framer.config.name}: Analysis completed")
        return notes

    async def continuous_record_and_transcribe(self, framer):
        print("Starting continuous recording. Press Ctrl+C to stop.")
        try:
            while True:
                transcription = await self.record_and_transcribe_audio()
                if transcription:
                    print(f"Transcription: {transcription}")
                    notes = await self.analyze_transcription(framer, transcription)
                    print(f"Actionable Notes: {notes}")
                await asyncio.sleep(1)  # Simulate waiting for the next input
        except KeyboardInterrupt:
            print("Continuous recording stopped.")
