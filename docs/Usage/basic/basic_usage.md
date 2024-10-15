# Basic Usage

This section provides a comprehensive guide on how to use the Frame framework to create and manage AI agents.

## Role and Goal Generation

When initializing a Framer, the behavior for role and goal generation is as follows:

- If both roles and goals are None, they will be automatically generated using `generate_roles_and_goals()`.
- If roles is an empty list `[]` and goals is None, only roles will be generated and set.
- If goals is an empty list `[]` and roles is None, only goals will be generated and set.
- If both roles and goals are empty lists `[]`, both will be generated and set.
- If either roles or goals is provided (not None or empty list), the provided value will be used, meaning the agent will have no roles or goals.

## Soul Seed

When creating a Framer, you can provide a soul_seed that can be either a string or a dictionary:

- If a string is provided, it will be used as the 'text' value in the soul's seed dictionary.
- If a dictionary is provided, it can include any keys and values, with an optional 'text' key for the soul's essence.

This allows for more flexible and detailed soul initialization.

## Prompt Formatting

When using different LLM adapters, it's important to format your prompts correctly:

- For LMQL: Use triple quotes and optionally specify the expected output format.
- For DSPy: Use standard string formatting.
- For Hugging Face: Use standard string formatting.
For detailed examples and explanations, see the [[prompt_examples]] documentation.

## Getting Started

1. **Initialize Frame**

   Start by importing and initializing the Frame class:

   ```python
   from frame import Frame

   frame = Frame()
   ```

2. **Create a Framer**

   Use the Frame instance to create a Framer with specific roles and goals:

   ```python
   config = {
       "name": "Example Framer",
       "default_model": "gpt-3.5-turbo"
   }
   roles = [{"name": "Assistant", "description": "Helps with tasks"}]
   goals = [{"description": "Complete tasks efficiently", "priority": 1.0}]

   framer = frame.create_framer(config, roles, goals)
   ```

3. **Interact with the Framer**

   You can now interact with the Framer to perform tasks and generate responses:

   ```python
   prompt = "What is the weather like today?"
   response = await framer.generate_response(prompt)
   print(response)
   ```

## Advanced Usage

- **Managing Workflows and Tasks**

  Framers can manage complex workflows and tasks. Use the Agency component to add and manage tasks:

  ```python
  task = {"description": "Analyze data", "priority": "high"}
  framer.agency.add_task(task)
  ```

- **Customizing the Framer**

  Customize the Framer's behavior by setting different roles, goals, and configurations.

## Next Steps

- [[index|Home]]
- [[installation]]
- [[Examples/index|Examples]]
- [[api_reference]]
- [[tests]]
- [[glossary]]
- [[cli_usage]]
- [[frame/framer/framer|Framer]]
