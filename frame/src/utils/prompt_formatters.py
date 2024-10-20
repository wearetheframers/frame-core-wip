from frame.src.services.llm.llm_adapters.lmql.lmql_interface import LMQLInterface

lmql_interface = LMQLInterface(model_name="gpt-3.5-turbo")


def format_lmql_prompt(prompt: str, expected_output: str = None) -> str:
    """
    Format a prompt for LMQL using the LMQL interface.

    Args:
        prompt (str): The input prompt.
        expected_output (str, optional): The expected output format.

    Returns:
        str: The formatted LMQL prompt.
    """
    constraints = []
    if expected_output:
        constraints.append(f"EXPECTED_OUTPUT in [{expected_output}]")
    return lmql_interface.format_prompt_with_constraints(prompt, constraints)


def format_dspy_prompt(prompt: str) -> str:
    """
    Format a prompt for DSPy.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The formatted DSPy prompt.
    """
    return prompt  # DSPy doesn't require special formatting


def format_huggingface_prompt(prompt: str) -> str:
    """
    Format a prompt for Hugging Face models.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The formatted Hugging Face prompt.
    """
    return prompt  # Hugging Face doesn't require special formatting
