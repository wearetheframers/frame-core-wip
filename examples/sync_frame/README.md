# SyncFrame Example

This example demonstrates how to use the `SyncFrame` class to interact with a `Framer` instance synchronously. The `SyncFrame` class provides a convenient way to use Frame in applications that do not support asynchronous programming.

## Running the Example

1. Ensure you have the necessary dependencies installed. You can install them using:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key in the `example.py` script:

   ```python
   llm_service = LLMService(api_key="your_api_key")
   ```

3. Run the example script:

   ```bash
   python example.py
   ```

## What the Example Does

- Initializes a `SyncFrame` instance with an `LLMService`.
- Creates a `Framer` instance using a configuration.
- Defines and performs a task synchronously.
- Processes a perception and makes a decision synchronously.
- Cleans up by closing the `Framer` instance.

This example provides a basic demonstration of how to use `SyncFrame` to manage tasks and perceptions in a synchronous manner.
