import logging
from typing import Any, Dict, List, Optional

from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.mem0_adapter import (
    Mem0Adapter,
)


class Mem0SearchExtractSummarizePlugin(BasePlugin):
    def __init__(self, framer):
        super().__init__(framer)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.mem0_adapter = Mem0Adapter()

    async def on_load(self) -> None:
        self.register_action(
            "mem0_search_extract_summarize",
            self.mem0_search_extract_summarize,
            "Search Mem0 for a query, extract information, and summarize the results. This action involves looking into the Framer's memories to retrieve relevant information and provide a comprehensive answer or share insights based on stored memories.",
        )

        # Add a new role for Mem0 searching and summarizing
        mem0_researcher_role = Role(
            name="Mem0 Researcher",
            description="Specializes in Mem0 searching, information extraction, and summarization",
            priority=Priority.HIGH,
            status=RoleStatus.ACTIVE,
        )
        self.framer.agency.add_role(mem0_researcher_role)

        # Add a new goal for providing comprehensive answers using Mem0
        comprehensive_answer_goal = Goal(
            name="Provide Comprehensive Answers using Mem0",
            description="Gather and synthesize information from Mem0 to provide comprehensive answers",
            priority=Priority.HIGH,
            status=GoalStatus.ACTIVE,
        )
        self.framer.agency.add_goal(comprehensive_answer_goal)

    def get_actions(self) -> Dict[str, Any]:
        """
        Return a dictionary of actions provided by this plugin.
        """
        return {
            "mem0_search_extract_summarize": self.mem0_search_extract_summarize
        }
        # Implement the execute method as required by BasePlugin
        pass

    async def execute(self, action_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a specified action with given parameters.

        Args:
            action_name (str): The name of the action to execute.
            parameters (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
        if action_name == "mem0_search_extract_summarize":
            return await self.mem0_search_extract_summarize(**parameters)
        else:
            raise ValueError(f"Action {action_name} not found in plugin.")

    async def mem0_search_extract_summarize(
        self,
        query: str,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        model_name: str = "gpt-4o-mini",
    ) -> str:
        self.logger.info(f"Searching Mem0 for query: {query}")

        # Ensure at least one required filter is provided
        if not any([user_id, agent_id, run_id]):
            user_id = "default"

        search_results = self.mem0_adapter.search(
            query, user_id=user_id, agent_id=agent_id, run_id=run_id, filters=filters
        )
        self.logger.info(f"Found {len(search_results)} results in Mem0")

        if not search_results:
            return "No relevant information found in Mem0."

        context = "\n".join([result["content"] for result in search_results])
        summary = await self.summarize(query, context, model_name)

        references = "\n".join(
            [f"[{i+1}] {result['id']}" for i, result in enumerate(search_results)]
        )
        return f"# Answer\n\n{summary}\n\n# References\n\n{references}"

    async def summarize(self, query: str, context: str, model_name: str) -> str:
        prompt = f"""
        Given the following context and query, provide a comprehensive answer:

        Context:
        {context}

        Query: {query}

        Answer:
        """

        system_message = "You are a helpful assistant that provides accurate and comprehensive answers based on the given context from Mem0."

        response = await self.framer.llm_service.get_completion(
            prompt,
            model=model_name,
            system_message=system_message,
            max_tokens=1000,
            temperature=0.5,
        )

        return response.strip()
