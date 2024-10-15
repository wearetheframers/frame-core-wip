import logging
from typing import Optional
from frame.src.framed.config import FramedConfig
from frame.src.services.llm.main import LLMService
from frame.src.framer.agency.agency import Agency
from frame.src.framer.brain.brain import Brain
from frame.src.framer.soul.soul import Soul
from frame.src.framer.agency.tasks.workflow.workflow_manager import WorkflowManager
from frame.src.services.memory.main import MemoryService
from frame.src.services.eq.main import EQService

logger = logging.getLogger(__name__)


class Framed:
    def __init__(
        self,
        config: FramedConfig,
        llm_service: LLMService,
        agency: Agency,
        brain: Brain,
        soul: Soul,
        workflow_manager: WorkflowManager,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ):
        self.config = config
        self.llm_service = llm_service
        self.agency = agency
        self.brain = brain
        self.soul = soul
        self.workflow_manager = workflow_manager
        self.memory_service = memory_service
        self.eq_service = eq_service
        logger.debug("Framed instance created")

    @classmethod
    async def create(
        cls,
        config: FramedConfig,
        llm_service: LLMService,
        soul_seed: Optional[str] = None,
        memory_service: Optional[MemoryService] = None,
        eq_service: Optional[EQService] = None,
    ) -> "Framed":
        agency = Agency(llm_service=llm_service, context=None)
        brain = Brain(
            llm_service=llm_service,
            default_model=config.default_model,
            roles=config.roles,
            goals=config.goals,
        )
        soul = Soul(seed=soul_seed or f"Default seed for {config.name}")
        workflow_manager = WorkflowManager()

        return cls(
            config=config,
            llm_service=llm_service,
            agency=agency,
            brain=brain,
            soul=soul,
            workflow_manager=workflow_manager,
            memory_service=memory_service,
            eq_service=eq_service,
        )

    async def sense(self, perception: dict) -> dict:
        # Implement perception processing logic here
        return await self.brain.process_perception(perception)

    async def perform_task(self, task: dict) -> dict:
        # Implement task execution logic here
        return await self.workflow_manager.execute_task(task)
