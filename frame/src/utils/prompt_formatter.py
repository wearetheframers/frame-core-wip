from typing import Dict, Any


def format_prompt(prompt: str) -> str:
    """
    Format a prompt for logging or debugging purposes.

    Args:
        prompt (str): The input prompt.

    Returns:
        str: The formatted prompt.
    """
    return f"Formatted Prompt: {prompt}"


def format_lmql_prompt(prompt: str, additional_context: Dict[str, Any] = None) -> str:
    """
    Format a prompt specifically for LMQL.

    Args:
        prompt (str): The input prompt.
        additional_context (Dict[str, Any], optional): Additional context for the prompt.

    Returns:
        str: The formatted LMQL prompt.
    """
    formatted_prompt = f'sample\n"{prompt}"\n[RESPONSE]'
    if additional_context:
        context_str = "\n".join(
            f"{key}: {value}" for key, value in additional_context.items()
        )
        formatted_prompt = f"{context_str}\n\n{formatted_prompt}"
    return formatted_prompt
