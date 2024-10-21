# Audio Transcription Example

This example demonstrates how to use the Frame framework to create a Framer that listens for mic input, records audio, transcribes it, and then analyzes the transcription to create actionable notes.

## Setup

1. Ensure you have the Frame framework installed and set up in your environment.

2. Navigate to the `examples/audio_transcription` directory.

## Running the Example

To run the audio transcription example, execute the following command:

```bash
python main.py
```

## How It Works

- The Framer is initialized with roles and goals:
  - **Roles**:
    - `Listener`: Responsible for listening to audio input and transcribing it.
    - `Analyzer`: Responsible for analyzing transcriptions to create actionable notes.
  - **Goals**:
    - `Transcribe Audio`: Accurately transcribe audio input.
    - `Generate Notes`: Create detailed notes from transcriptions.

- The `AudioTranscriptionPlugin` handles the recording and transcription of audio, as well as the analysis of the transcription to generate notes.

- The example simulates audio input and demonstrates how the Framer processes this input to achieve its goals.

## Customization

### Custom Action Registry

In the autonomous vehicle example, we demonstrate how to replace the default action registry with a custom one. This allows for a more flexible and hackable system where you can replace or extend default behaviors. The `process_perception` function takes precedence over the observe action, showing how you can customize the action registry. You can also remove actions from the Framer behavior in plugins programmatically.

You can customize the roles, goals, and behavior of the Framer by modifying the `main.py` and `audio_transcription_plugin.py` files.
