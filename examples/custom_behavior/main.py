from frame.src.framer.agency.action_registry import ActionRegistry


# Define a new custom action
def custom_greet_action(name: str) -> str:
    return f"Hello, {name}! Welcome to the custom behavior example."


# Register the custom action
action_registry = ActionRegistry()
action_registry.register_action(
    "custom_greet",
    custom_greet_action,
    description="Greet a user with a custom message",
    priority=5,
)

# Example usage of the custom action
if __name__ == "__main__":
    result = action_registry.perform_action("custom_greet", name="Alice")
    print(result)
