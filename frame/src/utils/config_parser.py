import json
import re
import os
from frame.src.framer.agency.priority import Priority
from typing import Dict, Any, Union, List, Type
from frame.src.framer.config import FramerConfig
from frame.src.services.context.execution_context_service import ExecutionContext
from frame.src.framer.agency.roles import Role
from frame.src.framer.agency.goals import Goal


def parse_json_config(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file:
        config_data = json.load(file)
    # Ensure actions are processed correctly
    if "actions" in config_data:
        for action in config_data["actions"]:
            # Standardize priority strings
            action["priority"] = action["priority"].upper()
    # Ensure priority is correctly parsed
    if "priority" in config_data:
        config_data["priority"] = Priority.get(config_data["priority"]).value
    return config_data


def parse_markdown_config(file_path: str) -> FramerConfig:
    with open(file_path, "r") as file:
        content = file.read()

    headers = re.findall(
        r"^##\s+(.*?)\n(.*?)(?=\n##|\Z)", content, re.DOTALL | re.MULTILINE
    )
    config_data = {}

    for header, value in headers:
        key = header.lower().replace(" ", "_")
        if key == "soul_traits":
            config_data[key] = [
                trait.strip() for trait in value.strip().split("-") if trait.strip()
            ]
        elif key in ["roles", "goals"]:
            config_data[key] = [
                {"name": item.strip(), "description": item.strip()}
                for item in value.strip().split("\n")
                if item.strip()
            ]
        elif key == "actions":
            actions = []
            action_entries = re.findall(
                r"-\s*Name:\s*(.*?)\n\s*Description:\s*(.*?)\n\s*Priority:\s*(.*?)\n",
                value + "\n",  # Ensure the regex processes the last entry
                re.DOTALL | re.MULTILINE,
            )
            for name, description, priority in action_entries:
                actions.append(
                    {
                        "name": name.strip(),
                        "description": description.strip(),
                        "priority": priority.strip().upper(),
                    }
                )
            config_data[key] = actions
            config_data[key] = value.strip()
    # Ensure priority is correctly parsed
    if "priority" in config_data:
        config_data["priority"] = Priority.get(config_data["priority"]).value
    return FramerConfig(**config_data)


def export_config_to_json(config: FramerConfig, file_path: str) -> None:
    with open(file_path, "w") as file:
        json.dump(config.dict(), file, indent=4)


def export_config_to_markdown(config: FramerConfig, file_path: str) -> None:
    with open(file_path, "w") as file:
        for key, value in config.dict().items():
            if key == "custom_script":
                continue  # Skip custom_script when exporting to markdown
            file.write(f"## {key.replace('_', ' ').title()}\n")
            if key == "soul_traits":
                for item in value:
                    file.write(f"- {item}\n")
            elif key == "soul_seed":
                file.write(f"{value['text']}\n")
            else:
                file.write(f"{value}\n")
            file.write("\n")


def execution_context_to_json(execution_context: ExecutionContext) -> Dict[str, Any]:
    """
    Convert an ExecutionContext object to a JSON-serializable dictionary.
    """
    return {
        "roles": [role.to_dict() for role in execution_context.get_roles()],
        "goals": [goal.to_dict() for goal in execution_context.get_goals()],
        "state": execution_context.state,
    }


def execution_context_from_json(
    data: Dict[str, Any], execution_context_cls: Type[ExecutionContext]
) -> ExecutionContext:
    """
    Create an ExecutionContext object from a JSON-serializable dictionary.
    """
    execution_context = execution_context_cls()
    execution_context.set_roles([Role(**role) for role in data.get("roles", [])])
    execution_context.set_goals([Goal(**goal) for goal in data.get("goals", [])])
    execution_context.state = data.get("state", {})
    return execution_context
