# Advanced Usage

This section provides a comprehensive guide on how to use the Frame framework to create and manage AI agents.

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

- [[index]]
- [[configuration]]
- [[api_reference]]
- [[framer]]
- [[agency]]
- [[brain]]
- [[soul]]
