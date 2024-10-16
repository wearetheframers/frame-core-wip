import os
from frame.src.utils.config_parser import load_framer_from_file
from frame.src.framer.framer import Framer
from frame.src.services.llm.main import LLMService

def main():
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    config_path = os.path.join(script_dir, 'config.json')

    # Load the Framer configuration from the JSON file
    config = load_framer_from_file(config_path)

    # Initialize the LLM service
    llm_service = LLMService()

    # Create a Framer instance
    framer = Framer.load_from_file(config_path, llm_service)

    # Perform tasks with the Framer
    # Example: framer.perform_task({"task": "example task"})

if __name__ == "__main__":
    main()
