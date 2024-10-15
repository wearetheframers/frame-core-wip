import asyncio
from frame.src.framer.framer import Framer
from frame.src.framer.config import FramerConfig
from frame.src.services.llm.main import LLMService


async def main():
    # Initialize the LLMService and FramerConfig
    llm_service = LLMService(openai_api_key="your_openai_api_key")
    config = FramerConfig(name="Example Framer", default_model="gpt-3.5-turbo")

    # Create a Framer instance
    framer = Framer(config=config, llm_service=llm_service)

    # Define a prompt
    prompt = "Write a short story about an AI learning to understand human emotions."

    # Perform a task with streaming enabled
    await framer.perform_task({"description": prompt})

    # Access the streamed response
    streamed_response = framer._streamed_response
    print("Streamed Response Status:", streamed_response["status"])
    print("Streamed Response Result:", streamed_response["result"])


if __name__ == "__main__":
    asyncio.run(main())
