# Framer Created from Markdown

This example demonstrates how to create a Framer instance from a Markdown configuration file. The Framer is configured with rich textual descriptions to enable engaging interactions.

## How Markdown Configuration Works

Markdown configuration allows you to define the setup of a Framer instance using a simple and human-readable format. Each section in the markdown file corresponds to a specific configuration aspect, such as roles, goals, or actions. This approach makes it easy to visualize and modify the configuration without delving into complex code structures.

### Structure of the Markdown File

- **Headers**: Use `##` to define sections like roles, goals, and actions.
- **Lists**: Use `-` to list items such as role names or action descriptions.
- **Key-Value Pairs**: Use `:` to separate keys and values within lists.

### Example Markdown Configuration

```markdown
## Roles
- Name: Listener
  Description: Listens to audio input and transcribes it.

## Goals
- Name: Transcribe Audio
  Description: Accurately transcribe audio input.

## Actions
- Name: Record Audio
  Description: Record audio from the microphone.
  Priority: High
```

## Adding More Complicated Examples

To add more complex examples, you can extend the markdown configuration with additional sections or more detailed descriptions. For instance, you can define complex actions with multiple parameters or nested goals with specific conditions.

### Example of a Complex Configuration

```markdown
## Roles
- Name: Advanced Listener
  Description: Listens to audio input, transcribes it, and analyzes sentiment.

## Goals
- Name: Analyze Sentiment
  Description: Determine the sentiment of transcribed audio.

## Actions
- Name: Record and Analyze Audio
  Description: Record audio, transcribe it, and analyze sentiment.
  Priority: Critical
  Parameters:
    - Duration: 10
    - SampleRate: 16000
```

## API Methods and Usage

The Framer API provides several methods to interact with the configuration and execute actions. Here are some key methods and how to use them:

### `create_framer`

Creates a new Framer instance based on the provided configuration.

```python
from frame import Frame, FramerConfig

frame = Frame()
config = FramerConfig(name="Example Framer")
framer = frame.create_framer(config)
```

### `execute_action`

Executes a specified action within the Framer.

```python
result = framer.brain.action_registry.execute_action("record_and_analyze_audio")
print(f"Action result: {result}")
```

### `add_role` and `add_goal`

Adds a new role or goal to the Framer's configuration.

```python
framer.agency.add_role({"name": "New Role", "description": "A new role description"})
framer.agency.add_goal({"name": "New Goal", "description": "A new goal description"})
```

## Why Use Markdown for Configuration?

Using markdown for configuration offers several benefits:

- **Readability**: Markdown is easy to read and write, making it accessible to non-developers.
- **Flexibility**: Easily modify configurations without changing the underlying code.
- **Portability**: Share configurations as simple text files that can be version-controlled and collaborated on.

## How to Run

1. Ensure you have all necessary dependencies installed.
2. Run the `main.py` script to see the Framer in action.

```bash
python main.py
```
