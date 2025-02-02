import time
from typing import Optional

class TokenBucket:
    """
    Implements token bucket algorithm for rate limiting.
    
    This class provides a token bucket rate limiting mechanism where tokens are added
    at a fixed rate up to a maximum capacity. Tokens are consumed when operations
    are performed.
    
    Attributes:
        capacity (int): Maximum number of tokens the bucket can hold
        tokens (float): Current number of tokens in the bucket
        rate (float): Rate at which tokens are added (tokens per second)
        last_update (float): Timestamp of last token update
    """
    
    def __init__(self, tokens: int, seconds: int):
        """
        Initialize the token bucket.
        
        Args:
            tokens (int): Maximum number of tokens (capacity)
            seconds (int): Time window in seconds for token replenishment
        """
        self.capacity = float(tokens)
        self.tokens = float(tokens)
        self.rate = float(tokens) / float(seconds)
        self.last_update = time.time()

    def _add_tokens(self) -> None:
        """Add tokens based on time elapsed since last update."""
        now = time.time()
        time_passed = now - self.last_update
        new_tokens = time_passed * self.rate
        
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_update = now

    def consume(self, tokens: int) -> bool:
        """
        Try to consume tokens from the bucket.
        
        Args:
            tokens (int): Number of tokens to consume
            
        Returns:
            bool: True if tokens were consumed, False if insufficient tokens
        """
        self._add_tokens()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def get_tokens(self) -> float:
        """
        Get current number of available tokens.
        
        Returns:
            float: Number of tokens currently available
        """
        self._add_tokens()
        return self.tokens
