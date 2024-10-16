import sys
import os

# Import Frame from upper dir
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import asyncio
from frame import Frame, FramerConfig


async def main():
    # Initialize the Frame and FramerConfig
    frame = Frame()
    config = FramerConfig(name="Example Framer", default_model="gpt-3.5-turbo")

    # Create a Framer instance
    framer = await frame.create_framer(config)

    # Define a prompt
    prompt = "Write a short story about an AI learning to understand human emotions."

    # Perform a task with streaming enabled
    result = await framer.prompt(prompt, stream=True)

    # Print the streamed response
    print("Streamed Response:")
    async for chunk in result:
        print(chunk, end="", flush=True)
    print("\n")

    # Access the final streamed response
    streamed_response = framer._streamed_response
    print("Final Streamed Response Status:", streamed_response["status"])
    print("Final Streamed Response Result:", streamed_response["result"])


if __name__ == "__main__":
    asyncio.run(main())
