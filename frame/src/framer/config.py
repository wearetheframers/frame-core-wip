from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


from dataclasses import dataclass, field
from typing import Optional

@dataclass
class FramerConfig:
    name: str
    model: Optional[str] = field(default=None)
    """
    Configuration class for Framer instances.

    This class initializes a Framer configuration based on a dictionary of settings.
    It uses the FramerConfigModel to validate and set default values for the configuration.

    Attributes:
        name (str): The name of the Framer.
        description (Optional[str]): The description of the Framer.
        singleton (Optional[bool]): Whether the Framer is a singleton instance.
        gender (Optional[str]): The gender of the Framer.
        default_model (Optional[str]): The default language model to use.
        multi_modal_model (Optional[str]): The multi-modal model to use.
        llm_temperature (Optional[float]): The temperature setting for language model responses.
        llm_max_tokens (Optional[int]): The maximum number of tokens for language model responses.
        llm_top_p (Optional[float]): The top_p setting for language model responses.
        llm_frequency_penalty (Optional[float]): The frequency penalty for language model responses.
        llm_presence_penalty (Optional[float]): The presence penalty for language model responses.
        is_multi_modal (Optional[bool]): Indicates if multi-modal capabilities are enabled.
        roles (Optional[List[Dict[str, str]]]): The roles for the Framer.
        goals (Optional[List[Dict[str, Any]]]): The goals for the Framer.
    """

    name: str
    description: Optional[str] = None
    singleton: Optional[bool] = False
    gender: Optional[str] = "neutral"
    default_model: Optional[str] = "gpt-3.5-turbo"
    multi_modal_model: Optional[str] = "gpt-4-vision-preview"
    llm_temperature: Optional[float] = 0.7
    llm_max_tokens: Optional[int] = 1024
    llm_top_p: Optional[float] = 1.0
    llm_frequency_penalty: Optional[float] = 0.0
    llm_presence_penalty: Optional[float] = 0.0
    is_multi_modal: Optional[bool] = False
    roles: Optional[List[Dict[str, str]]] = field(default_factory=list)
    goals: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    async def initialize(self):
        """Initialize the Framer with roles and goals."""
        if self.agency.roles is None and self.agency.goals is None:
            self.agency.roles, self.agency.goals = await self.agency.generate_roles_and_goals()
        elif self.agency.roles == [] and self.agency.goals is None:
            _, self.agency.goals = await self.agency.generate_roles_and_goals()
        elif self.agency.goals == [] and self.agency.roles is None:
            self.agency.roles, _ = await self.agency.generate_roles_and_goals()
        elif self.agency.roles == [] and self.agency.goals == []:
            self.agency.roles, self.agency.goals = await self.agency.generate_roles_and_goals()
        
        # Ensure goals are generated if they are None
        if self.agency.goals is None:
            _, self.agency.goals = await self.agency.generate_roles_and_goals()

        # Ensure roles are generated if they are None
        if self.agency.roles is None:
            self.agency.roles, _ = await self.agency.generate_roles_and_goals()
