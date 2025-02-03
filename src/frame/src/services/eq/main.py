from frame.src.services.eq.eq_adapters import SentimentAnalysisAdapter


class EQService:
    """
    EQ (Emotional Intelligence) Service for managing emotional intelligence capabilities.
    """

    def __init__(self):
        self.adapter = SentimentAnalysisAdapter()

    def analyze_text(self, text: str):
        """
        Analyze the given text for emotional content.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: The emotional state detected in the text.
        """
        return self.adapter.analyze(text)
