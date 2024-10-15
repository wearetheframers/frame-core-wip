import uuid


def generate_id() -> str:
    """
    Generate a unique identifier.

    Returns:
        str: A unique identifier string.
    """
    return str(uuid.uuid4())
