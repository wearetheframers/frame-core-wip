"""
Mem0SearchExtractSummarizePlugin

This plugin provides a mechanism to look into memories, retrieve relevant information, and share insights,
functioning as a Retrieval-Augmented Generation (RAG) mechanism. It is automatically included when the
'with-memory' permission is granted to a Framer, ensuring that memory-based responses are comprehensive
and contextually relevant.

Note: This plugin might be refactored into a core component in the future to streamline its integration
and usage within the Frame framework.
"""

import logging
import os
from frame.src.services.context.execution_context_service import ExecutionContext
from typing import Any, Dict, List, Optional

from frame.src.framer.brain.plugins.base import BasePlugin
from frame.src.framer.agency.goals import Goal, GoalStatus
from frame.src.framer.agency.roles import Role, RoleStatus
from frame.src.framer.agency.priority import Priority
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.mem0_adapter import (
    Mem0Adapter,
)

from frame.src.constants import MEM0_API_KEY


class Mem0SearchExtractSummarizePlugin(BasePlugin):
    def __init__(self, framer):
        super().__init__(framer)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'))
        self.logger.addHandler(handler)
        self.mem0_adapter = Mem0Adapter()

    async def on_load(self, framer) -> None:
        # Check for a valid API key before registering the action
        api_key = os.getenv("MEM0_API_KEY", "").strip()
        if not api_key:
            api_key = MEM0_API_KEY
        if api_key:
            framer.agency.action_registry.add_action(
                "respond with memory retrieval",
                description="This action is ideal for responding to personal questions that involve historical or memory-based "
                            "information about the user or the Framer. It leverages the Framer's memory to retrieve relevant data "
                            "or previously saved texts, providing comprehensive answers or insights based on stored memories. "
                            "When questions reference or relate to past conversations, this action is preferred. It generally "
                            "takes precedence over `think` and `observe` actions, especially for questions. If uncertain whether "
                            "a question can be answered with or without memory, default to this action.",
                action_func=self.mem0_search_extract_summarize,
                priority=8,
            )
            self.logger.info("Mem0SearchExtractSummarizePlugin registered 'response with memory retrieval' action.")
            # Remove respond action
            if "respond" in framer.agency.action_registry.get_all_actions():
                framer.agency.action_registry.remove_action("respond")
            else:
                self.logger.warning("Action 'respond' not found in registry. Skipping removal.")
        else:
            self.logger.warning("Mem0 API key not found or is empty. Action 'response with memory retrieval' will not be registered.")

        # # Add a new role for Mem0 searching and summarizing
        # mem0_researcher_role = Role(
        #     name="Mem0 Researcher",
        #     description="Specializes in Mem0 searching, information extraction, and summarization",
        #     priority=Priority.HIGH,
        #     status=RoleStatus.ACTIVE,
        # )
        # self.framer.agency.add_role(mem0_researcher_role)

        # # Add a new goal for providing comprehensive answers using Mem0
        # comprehensive_answer_goal = Goal(
        #     name="Provide Comprehensive Answers using Mem0",
        #     description="Gather and synthesize information from Mem0 to provide comprehensive answers",
        #     priority=Priority.HIGH,
        #     status=GoalStatus.ACTIVE,
        # )
        # self.framer.agency.add_goal(comprehensive_answer_goal)

    def get_actions(self) -> Dict[str, Any]:
        """
        Return a dictionary of actions provided by this plugin.
        """
        return {
            "respond with memory retrieval": self.mem0_search_extract_summarize
        }

    async def execute(self, action_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a specified action with given parameters.

        Args:
            action_name (str): The name of the action to execute.
            parameters (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
        if action_name == "respond with memory retrieval":
            return await self.mem0_search_extract_summarize(**parameters)
        else:
            raise ValueError(f"Action {action_name} not found in plugin.")
        
    def filter_search_results(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter search results by memory text to remove duplicate results.

        Args:
            search_results (List[Dict[str, Any]]): List of search results.

        Returns:
            List[Dict[str, Any]]: Filtered list of search results.
        """
        memory_texts = set()
        filtered_results = []
        for result in search_results:
            if isinstance(result, dict) and "content" in result and isinstance(result["content"], dict) and "memory" in result["content"]:
                memory_text = result["content"]["memory"]
                if memory_text not in memory_texts:
                    memory_texts.add(memory_text)
                    filtered_results.append(result)
        return filtered_results

    async def mem0_search_extract_summarize(
        self,
        query: str = "",
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        model_name: str = "gpt-4o-mini",
        text_response: Optional[str] = None,
    ) -> str:
        if not query:
            raise ValueError("Query cannot be null or empty.")
        # Ensure the query is a string
        if not isinstance(query, str):
            query = str(query)
        self.logger.info(f"Searching Mem0 for query: {query}")

        # Ensure at least one required filter is provided
        if not any([user_id, agent_id, run_id]):
            user_id = "default"

        search_results = self.mem0_adapter.search(
            query, user_id=user_id, agent_id=agent_id, run_id=run_id, filters=filters
        )
        self.logger.info(f"Found {len(search_results)} results in Mem0")
        self.logger.debug(f"Search results: {search_results}")

        if not search_results:
            return "No relevant information found in Mem0."
        
        # Filter search results by memory text (remove same text results)
        search_results = self.filter_search_results(search_results)
        self.logger.debug(f"Filtered search results: {search_results}")

        context = "\n".join([result["content"]["memory"] for result in search_results if isinstance(result, dict) and "content" in result and isinstance(result["content"], dict) and "memory" in result["content"]])
        if not context:
            return "No relevant information found in Mem0."

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


        response = await self.framer.llm_service.get_completion(
            prompt,
            model=model_name,
            max_tokens=1000,
            temperature=0.5,
        )

        return response.strip()
