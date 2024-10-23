from setuptools import setup, find_packages

setup(
    name="audio_transcription_plugin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sounddevice",
        "numpy",
        "whisper",
    ],
    entry_points={
        "console_scripts": [
            "audio_transcription=audio_transcription_plugin:main",
        ],
    },
)
