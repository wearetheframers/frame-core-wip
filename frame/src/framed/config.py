from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class FramedConfig:
    """
    Configuration class for Framed instances.

    This class initializes a Framed configuration based on a dictionary of settings.
    It uses the FramedConfigModel to validate and set default values for the configuration.

    Attributes:
        name (str): The name of the Framed.
        description (Optional[str]): The description of the Framed.
        default_model (Optional[str]): The default language model to use.
        llm_temperature (Optional[float]): The temperature setting for language model responses.
        llm_max_tokens (Optional[int]): The maximum number of tokens for language model responses.
        roles (Optional[List[Dict[str, str]]]): The roles for the Framed.
        goals (Optional[List[Dict[str, Any]]]): The goals for the Framed.
    """

    name: str
    description: Optional[str] = None
    default_model: Optional[str] = "gpt-3.5-turbo"
    llm_temperature: Optional[float] = 0.7
    llm_max_tokens: Optional[int] = 1024
    roles: Optional[List[Dict[str, str]]] = field(default_factory=list)
    goals: Optional[List[Dict[str, Any]]] = field(default_factory=list)


# Example configuration for FramedConfig
example_framed_config = FramedConfig(
    name="ExampleFramed",
    description="An example Framed instance for demonstration purposes",
    default_model="gpt-3.5-turbo",
    llm_temperature=0.8,
    llm_max_tokens=2048,
    roles=[
        {"name": "Assistant", "description": "Helps with various tasks"},
        {"name": "Analyst", "description": "Analyzes data and provides insights"},
    ],
    goals=[
        {"description": "Assist users effectively", "priority": 1.0},
        {"description": "Provide accurate information", "priority": 0.9},
    ],
)
