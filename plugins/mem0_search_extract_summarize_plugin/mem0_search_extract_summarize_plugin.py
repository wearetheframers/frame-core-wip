"""
Mem0SearchExtractSummarizePlugin

This plugin provides a mechanism to search memories, extract relevant information, and generate summarized insights,
functioning as a Retrieval-Augmented Generation (RAG) mechanism. It is automatically included when the
'with-memory' permission is granted to a Framer, ensuring that memory-based responses are comprehensive
and contextually relevant.

The plugin enhances the Framer's ability to provide informed responses by leveraging stored memories
and contextual information. It integrates seamlessly with the Mem0 memory system to facilitate
efficient memory retrieval and summarization.

Key features:
- Memory search based on user queries
- Relevant information extraction from memories
- Summarization of extracted information
- Integration with the Framer's action registry for easy invocation

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
from frame.src.framer.brain.decision import Decision
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter.mem0_adapter import (
    Mem0Adapter,
)

from frame.src.constants import MEM0_API_KEY


class Mem0SearchExtractSummarizePlugin(BasePlugin):
    def __init__(self, framer=None):
        super().__init__(framer)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
            )
        )
        self.logger.addHandler(handler)
        self.mem0_adapter = Mem0Adapter()

    async def on_load(self, framer) -> None:
        # Check for the correct permission before registering the action
        if "with_mem0_search_extract_summarize_plugin" in framer.permissions:
            api_key = os.getenv("MEM0_API_KEY", "").strip()
            if not api_key:
                api_key = MEM0_API_KEY
            if api_key:
                framer.brain.action_registry.add_action(
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
                self.logger.info(
                    "Mem0SearchExtractSummarizePlugin registered 'respond with memory retrieval' action."
                )
            else:
                self.logger.warning(
                    "Mem0 API key not found or is empty. Action 'response with memory retrieval' will not be registered."
                )
        else:
            self.logger.info(
                "Mem0SearchExtractSummarizePlugin not loaded due to missing permission."
            )

    def get_actions(self) -> Dict[str, Any]:
        """
        Return a dictionary of actions provided by this plugin.
        """
        return {"respond with memory retrieval": self.mem0_search_extract_summarize}

    async def execute(self, action_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Execute a specified action with given parameters.

        Args:
            action_name (str): The name of the action to execute.
            parameters (Dict[str, Any]): Parameters for the action.

        Returns:
            Any: The result of the action execution.
        """
        self.logger.debug(
            f"Executing action: {action_name} with parameters: {parameters}"
        )
        if action_name == "respond with memory retrieval":
            self.logger.info("Executing 'respond with memory retrieval' action.")
            query = parameters.get("memory_question") or parameters.get("text", "") or parameters.get("query", "")
            execution_context = parameters.get("execution_context") or self.framer.execution_context
            llm_service = parameters.get("llm_service") or (execution_context.llm_service if execution_context else None)
        
            if not llm_service:
                raise ValueError("LLM service is required but not provided")
            
            return await self.mem0_search_extract_summarize(
                query=query,
                execution_context=execution_context,
                llm_service=llm_service,
                **parameters
            )
        else:
            raise ValueError(f"Action {action_name} not found in plugin.")

    def filter_search_results(
        self, search_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
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
            if (
                isinstance(result, dict)
                and "content" in result
                and isinstance(result["content"], dict)
                and "memory" in result["content"]
            ):
                memory_text = result["content"]["memory"]
                if memory_text not in memory_texts:
                    memory_texts.add(memory_text)
                    filtered_results.append(result)
        return filtered_results

    async def mem0_search_extract_summarize(
        self,
        execution_context: Optional[ExecutionContext] = None,
        query: str = "",
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        run_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        model_name: str = "gpt-4o-mini",
        text_response: Optional[str] = None,
        llm_service: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        self.logger.debug(f"mem0_search_extract_summarize called with query: '{query}'")
        self.logger.debug(f"Parameters received: {kwargs}")
        self.logger.debug(f"Execution context: {execution_context}")
        self.logger.debug(f"Query before processing: '{query}'")
        self.logger.debug(f"Execution context: {execution_context}")
        if not query or not isinstance(query, str) or query.strip() == "":
            self.logger.warning(
                f"Query is empty or invalid: '{query}'. Returning default response."
            )
            return {
                "action": "respond",
                "parameters": {
                    "response": "Query is empty. Please provide a valid query to search for relevant information."
                },
                "reasoning": "Empty query provided.",
                "confidence": 0.5,
                "priority": 1,
                "related_roles": [],
                "related_goals": [],
            }

        if execution_context is None:
            execution_context = self.framer.execution_context

        if not isinstance(execution_context, ExecutionContext):
            self.logger.error("Execution context is not properly initialized.")
            return {
                "error": "Execution context is not properly initialized.",
                "fallback_response": "An error occurred while processing your request. Please try again.",
            }

        # Ensure the query is a string
        if not isinstance(query, str):
            query = str(query)
        self.logger.debug(f"Searching Mem0 for query: {query}")

        # Ensure at least one required filter is provided
        if not any([user_id, agent_id, run_id]):
            user_id = "default"

        self.logger.debug(
            f"Searching with user_id: {user_id}, agent_id: {agent_id}, run_id: {run_id}"
        )
        search_results = self.mem0_adapter.search(
            query, user_id=user_id, agent_id=agent_id, run_id=run_id, filters=filters
        )
        self.logger.debug(f"Found {len(search_results)} results in Mem0")
        self.logger.debug(f"Search results: {search_results}")

        if not search_results:
            return {
                "action": "respond",
                "parameters": {
                    "response": "I don't have any specific information about that in my memory. Is there anything else I can help you with?"
                },
                "reasoning": "No relevant information found in memory.",
                "confidence": 0.5,
                "priority": 1,
                "related_roles": [],
                "related_goals": [],
            }

        # Filter search results by memory text (remove same text results)
        search_results = self.filter_search_results(search_results)

        context = "\n".join(
            [
                result["content"]["memory"]
                for result in search_results
                if isinstance(result, dict)
                and "content" in result
                and isinstance(result["content"], dict)
                and "memory" in result["content"]
            ]
        )
        if not context:
            return "No relevant information found in Mem0."

        summary = await self.summarize(query, context, model_name, llm_service)

        references = "\n".join(
            [f"[{i+1}] {result['id']}" for i, result in enumerate(search_results)]
        )
        self.logger.info(f"Memory retrieval response: {summary}")
        return summary

    async def summarize(self, query: str, context: str, model_name: str, llm_service: Any) -> str:
        prompt = f"""
        Given the following context and query, provide a comprehensive answer:

        Context:
        {context}

        Query: {query}

        Answer:
        """

        if not llm_service:
            raise ValueError("LLM service is required but not provided")
            
        response = await llm_service.get_completion(
            prompt,
            model=model_name,
            max_tokens=1000,
            temperature=0.5,
        )

        return response.strip()
