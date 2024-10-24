# Audio Transcription Plugin

This plugin provides audio transcription capabilities using the Whisper model. It can record audio, transcribe it, and analyze the transcription to create actionable notes.

## Features

- Record and transcribe audio
- Analyze transcriptions to create notes
- Continuous monitoring of audio for sounds above a certain decibel level
- Optional transcription of detected sounds

## Installation

To install the plugin, run:

```bash
pip install .
```

## Usage

To use the plugin, you can run the following command:

```bash
audio_transcription
```

This will start the audio transcription process.

## Requirements

- sounddevice
- numpy
- whisper

Ensure these dependencies are installed in your environment.
