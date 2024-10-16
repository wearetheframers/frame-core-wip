import json
import re
import os
from typing import Dict, Any, Union, List
from frame.src.framer.config import FramerConfig


def parse_json_config(file_path: str) -> FramerConfig:
    with open(file_path, "r") as file:
        config_data = json.load(file)
    return FramerConfig(**config_data)


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
        elif key == "soul_seed":
            config_data[key] = {"text": value.strip()}
        else:
            config_data[key] = value.strip()

    # # Check for a Python script in the same directory
    # dir_path = os.path.dirname(file_path)
    # py_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and f != '__init__.py']
    # if py_files:
    #     config_data['custom_script'] = os.path.join(dir_path, py_files[0])

    return FramerConfig(**config_data)

    if not file_path.endswith((".json", ".md")):
        raise ValueError("Unsupported file format. Please use .json or .md files.")


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
