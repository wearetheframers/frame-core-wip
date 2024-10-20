import lmql
from typing import Optional, Callable, Dict, Any, List
from lmql.runtime.program_state import ProgramState
from lmql import decorators


class LMQLInterface:
    def __init__(self, model_name: str):
        self.model = lmql.model(model_name)

    def format_prompt_with_constraints(
        self, prompt: str, constraints: list, distribution: bool = False
    ) -> str:
        """
        Format a prompt with LMQL constraints and optionally include a distribution clause.

        Args:
            prompt (str): The input prompt.
            constraints (list): A list of constraints to apply.
            distribution (bool): Whether to include a distribution clause.

        Returns:
            str: The formatted prompt with constraints and optional distribution.
        """
        constraints_str = " AND ".join(constraints)
        distribution_clause = "\ndistribution" if distribution else ""
        return f"{prompt}\nConstraints: {constraints_str}{distribution_clause}"

    def clean_response(self, response: str) -> str:
        """
        Clean the response by removing unwanted text patterns.

        Args:
            response (str): The raw response from the language model.

        Returns:
            str: The cleaned response.
        """
        unwanted_patterns = ["Response:\n", "[RESPONSE]"]
        for pattern in unwanted_patterns:
            response = response.replace(pattern, "")
        return response.strip()

    def set_decoder(
        self,
        decoder: Optional[str] = None,
        decoder_params: Optional[Dict[str, Any]] = None,
    ):
        """
        Set the decoding algorithm and its parameters.

        Args:
            decoder (Optional[str]): The decoding algorithm to use.
            decoder_params (Optional[Dict[str, Any]]): Parameters for the decoding algorithm.
        """
        self.decoder = decoder
        self.decoder_params = decoder_params

    def apply_decorators(
        self, value: str, decorators: List[Callable], context: Any
    ) -> str:
        """
        Apply a list of decorators to a value.

        Args:
            value (str): The value to be decorated.
            decorators (List[Callable]): A list of decorator functions.
            context (Any): The context in which the decorators are applied.

        Returns:
            str: The decorated value.
        """
        for decorator in decorators:
            value = decorator(value, context)
        return value

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        constraints: list = None,
        distribution: bool = False,
        control_flow: Optional[Callable] = None,
        decorators: Optional[List[Callable]] = None,
    ) -> str:
        """
        Generate a response using LMQL with constraints and optionally obtain a distribution.
        Supports dynamic prompt construction with control flow.

        Args:
            prompt (str): The input prompt.
            max_tokens (int): Maximum number of tokens to generate.
            constraints (list, optional): Constraints to apply during generation.
            distribution (bool): Whether to obtain a distribution over possible values.
            control_flow (Callable, optional): A function to dynamically construct the prompt with control flow.

        Returns:
            str: The generated response or distribution.
        """
        if control_flow:
            prompt = control_flow(prompt)
        context = ProgramState(prompt)  # Pass the prompt to ProgramState
        if decorators:
            prompt = self.apply_decorators(prompt, decorators, context)
            prompt = self.format_prompt_with_constraints(
                prompt, constraints, distribution
            )
        if distribution:
            return await self.model.score(prompt, max_tokens=max_tokens)
        else:
            # Apply LMQL constraints during generation
            lmql_constraints = self._apply_lmql_constraints(constraints)
            return await self.model.generate(
                prompt, max_tokens=max_tokens, constraints=lmql_constraints
            )

    def _apply_lmql_constraints(self, constraints: list) -> list:
        """
        Convert user-defined constraints into LMQL-compatible constraints.

        Args:
            constraints (list): A list of user-defined constraints.

        Returns:
            list: A list of LMQL-compatible constraints.
        """
        lmql_constraints = []
        for constraint in constraints:
            if isinstance(constraint, str):
                lmql_constraints.append(constraint)
            elif isinstance(constraint, tuple) and len(constraint) == 2:
                constraint_type, value = constraint
                if constraint_type == "STOPS_AT":
                    lmql_constraints.append(f"STOPS_AT({value[0]}, {value[1]})")
                elif constraint_type == "INT":
                    lmql_constraints.append(f"INT({value})")
                elif constraint_type == "CHOICE":
                    lmql_constraints.append(f"{value[0]} in set({value[1]})")
                elif constraint_type == "LEN":
                    lmql_constraints.append(f"len({value[0]}) < {value[1]}")
                elif constraint_type == "TOKENS":
                    lmql_constraints.append(f"len(TOKENS({value[0]})) < {value[1]}")
                elif constraint_type == "REGEX":
                    lmql_constraints.append(f"REGEX({value[0]}, r'{value[1]}')")
        return lmql_constraints

    async def score(self, prompt: str, values: list) -> dict:
        """
        Score different continuation values for a given prompt.

        Args:
            prompt (str): The prompt to use as a common prefix for all continuations.
            values (list): The continuation values to score.

        Returns:
            dict: A dictionary with scores for each continuation.
        """
        return await self.model.score(prompt, values)
