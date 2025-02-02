from typing import Optional
from pydantic import BaseModel, Field

class LLMConfig(BaseModel):
    """Base configuration for LLM operations."""
    model: str = Field(default="gpt-3.5-turbo", description="The model to use")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    top_p: float = Field(default=1.0, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, description="Presence penalty")
    rate_limit_tokens: int = Field(default=60000, description="Token rate limit per time window")
    rate_limit_seconds: int = Field(default=60, description="Time window in seconds for rate limiting")
    timeout: Optional[float] = Field(default=30.0, description="Timeout in seconds for API calls")
    retry_count: int = Field(default=3, description="Number of retries for failed API calls")
from typing import Optional
from pydantic import BaseModel, Field

class LLMConfig(BaseModel):
    """Base configuration for LLM operations."""
    model: str = Field(default="gpt-3.5-turbo", description="The model to use")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    top_p: float = Field(default=1.0, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, description="Presence penalty")
    rate_limit_tokens: int = Field(default=60000, description="Token rate limit per time window")
    rate_limit_seconds: int = Field(default=60, description="Time window in seconds for rate limiting")
    timeout: Optional[float] = Field(default=30.0, description="Timeout in seconds for API calls")
    retry_count: int = Field(default=3, description="Number of retries for failed API calls")
