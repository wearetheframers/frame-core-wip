import os, sys

# Add the project root to the Python path to ensure all modules can be imported correctly
# If we are running the examples from the source code (not installing package from pip)
# then you need to have this line uncommented.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from frame.sync_frame import SyncFrame
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService

def main():
    # Initialize SyncFrame with an LLMService
    llm_service = LLMService()
    sync_frame = SyncFrame(llm_service=llm_service)

    # Create a Framer instance
    config = FramerConfig(name="Example Framer", default_model="gpt-4o-mini")
    framer = sync_frame.create_framer(config)

    # Define a task
    task = {"description": "Engage in a deep conversation"}
    result = sync_frame.perform_task(framer, task)
    print(f"Task result: {result}")

    # Process a perception
    perception = {"type": "hearing", "data": {"text": "Hello, how are you?"}}
    decision = sync_frame.process_perception(framer, perception)
    print(f"Decision: {decision}")

    # Clean up
    sync_frame.close_framer(framer)

if __name__ == "__main__":
    main()
