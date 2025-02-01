from typing import Dict, Any


class SentimentAnalysisAdapter:
    """
    A basic sentiment analysis adapter that tracks emotional state and detects emotions from text.
    """

    def __init__(self):
        self.emotional_state = {
            "happiness": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze the given text and update the emotional state.

        Args:
            text (str): The text to analyze.

        Returns:
            Dict[str, Any]: The detected emotions and their intensities.
        """
        # Placeholder logic for sentiment analysis
        # In a real implementation, this would involve NLP techniques
        if "happy" in text:
            self.emotional_state["happiness"] += 0.1
        if "sad" in text:
            self.emotional_state["sadness"] += 0.1
        if "angry" in text:
            self.emotional_state["anger"] += 0.1
        if "fear" in text:
            self.emotional_state["fear"] += 0.1
        if "surprised" in text:
            self.emotional_state["surprise"] += 0.1
        if "disgusted" in text:
            self.emotional_state["disgust"] += 0.1

        return self.emotional_state

    def reset_emotional_state(self):
        """
        Reset the emotional state to neutral.
        """
        for emotion in self.emotional_state:
            self.emotional_state[emotion] = 0.0
