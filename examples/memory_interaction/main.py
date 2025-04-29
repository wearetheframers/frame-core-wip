import asyncio
import os, sys
import json
import random
import logging

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the API key from config.json
curr_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(curr_dir, "config.json")
with open(config_path, "r") as f:
    config = json.load(f)
    os.environ["MEM0_API_KEY"] = config.get("MEM0_API_KEY", "")

# Import Frame after setting the environment variable
from frame import Frame
from frame.src.framer.config import FramerConfig
from frame.src.framer.brain.memory.memory_adapters.mem0_adapter import Mem0Adapter
from frame.src.services import MemoryService

async def main():
    # Initialize Frame with the API key from config
    frame = Frame()
    
    # Create a memory adapter with explicit API key
    mem0_api_key = config.get("MEM0_API_KEY")
    memory_adapter = Mem0Adapter(api_key=mem0_api_key)
    
    # Create a FramerConfig with the necessary permissions
    framer_config = FramerConfig(
        name="Memory Demo",
        default_model="gpt-4o-mini",
        permissions=[
            "with_memory",
            "with_mem0_search_extract_summarize_plugin",
            "with_shared_context",
        ],
        mem0_api_key=mem0_api_key,
    )
    
    # Create a Framer
    framer = await frame.create_framer(framer_config)
    
    # Replace the memory service with our adapter
    memory_service = MemoryService(adapter=memory_adapter)
    framer.brain.set_memory_service(memory_service)
    
    # Store some memories
    print("\n--- Storing memories ---")
    user_id = "default"
    if framer.brain and framer.brain.memory:
        framer.brain.memory.store("My favorite color is blue.", user_id=user_id)
        framer.brain.memory.store("I have a dentist appointment on October 20th.", user_id=user_id)
        framer.brain.memory.store("I plan to visit Hawaii for my vacation.", user_id=user_id)
        print("Memories stored successfully.")
    
    # Prepare some queries
    queries = [
        "What is my favorite color?",
        "When is my next appointment?",
        "What did I say about my vacation plans?",
        "What is the capital of France?",
        "How many continents are there?",
        "What is the boiling point of water in Celsius?",
    ]
    
    # Process each query and print results
    random.shuffle(queries)
    for query in queries:
        print(f"\n--- Query: {query} ---")
        
        # Create a perception from the query
        perception = {"type": "hearing", "data": {"text": query}}
        
        # Process the perception and get a decision
        decision = await framer.sense(perception)
        if decision:
            # Extract the parameters and action
            if decision.action == "respond":
                if "response" in decision.parameters:
                    print("\nResponse:")
                    print(decision.parameters["response"])
                else:
                    # Get the default response from an LLM
                    response = await frame.get_completion(query)
                    print("\nResponse:")
                    print(response)
            elif decision.action == "respond with memory retrieval":
                # Execute the memory retrieval action directly
                query_text = query
                result = await framer.brain.action_registry.execute_action(
                    "respond with memory retrieval", 
                    query=query_text,
                    user_id=user_id,
                    llm_service=frame.llm_service
                )
                print("\nResponse from Memory:")
                print(result)
            else:
                print(f"\nAction: {decision.action}")
                print(f"Parameters: {decision.parameters}")
        else:
            print("No decision was made.")

if __name__ == "__main__":
    asyncio.run(main())