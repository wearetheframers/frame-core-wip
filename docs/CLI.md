---
weight: 10
---

# CLI

The Frame CLI provides a command-line interface for interacting with the Frame system. It allows you to run Framers, launch the TUI, and perform various operations using command-line options.

## CLI Commands

### General Options

- `--openai-api-key`: OpenAI API key.
- `--mistral-api-key`: Mistral API key.
- `--huggingface-api-key`: Hugging Face API key.
- `--debug`: Enable debug logging.
- `--default-model`: Set the default model for all operations.

### Commands

#### `run-framer`

Run a Framer with a custom name and model.

```bash
python -m frame.cli run-framer --name "Research Assistant" --model "gpt-4" --prompt "What are the best open-source cognitive AI agent libraries in 2024?"
```

#### `run-framer-json`

Run a Framer with JSON input.

```bash
# Run a Framer with a perception input
python -m frame.cli run-framer-json '{"perception": {"type": "visual", "data": {"object": "tree"}, "source": "camera"}}'
```

#### `run-framer-json` in synchronous mode

Run a Framer with JSON input in synchronous mode.

```bash
python -m frame.cli run-framer-json --sync '{"prompt": "Explain the concept of quantum computing"}'
```

#### `run-framer-json` with streaming output

Run a Framer with JSON input and streaming output.

```bash
python -m frame.cli run-framer-json --stream '{"prompt": "Generate a step-by-step guide for baking a chocolate cake"}'
```

#### `run-framer` in synchronous mode

Run a Framer in synchronous mode.

```bash
python -m frame.cli run-framer --sync --prompt "Explain the difference between synchronous and asynchronous programming"
```

#### `run-framer` with streaming output

Run a Framer with streaming output.

```bash
python -m frame.cli run-framer --stream --prompt "Write a short story about an AI learning to understand human emotions"
```

### TUI

Launch the Text-based User Interface (TUI).

```bash
python -m frame.cli tui
```

## CLI Help

The Frame CLI provides a help command to display available options and commands. Use the following command to view the help information:

```bash
python -m frame.cli --help
```

To turn on debug logging, run the CLI with `--debug`.

## TUI

The Text-based User Interface (TUI) provides an interactive way to interact with the Frame system. It allows you to manage tasks, view logs, and perform other operations in a text-based environment.

Once launched, you can navigate through the interface using keyboard shortcuts and commands specific to the TUI environment.
