"""
CLI module for the Frame framework.

This module provides command-line interface (CLI) commands for interacting with
the Frame framework. It includes commands for running Framers, managing configurations,
and executing tasks.

Attributes:
    logger (Logger): Logger instance for logging CLI activities.
"""

import click
import json
import asyncio
import logging
from frame.frame import Frame
from frame.src.framed.config import FramedConfig

logger = logging.getLogger(__name__)


@click.group(help="Frame CLI for quick testing and interaction.")
@click.option("--debug/--no-debug", default=False, help="Enable debug logging")
@click.pass_context
def cli(ctx, debug):
    """Frame CLI tool."""
    ctx.ensure_object(dict)
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.setLevel(log_level)
    if debug:
        logger.debug("Debug mode is enabled")


def process_json_input(json_input: str) -> dict:
    """
    Process JSON input for Framer configuration.

    Args:
        json_input (str): JSON string containing Framer configuration.

    Returns:
        dict: Parsed JSON data as a dictionary.

    Raises:
        click.UsageError: If JSON is invalid or required fields are missing.
    """
    try:
        data = json.loads(json_input)
    except json.JSONDecodeError:
        raise click.UsageError("Invalid JSON format for input")

    if not data.get("prompt") and not data.get("perception"):
        raise click.UsageError(
            "Either 'prompt' or 'perception' must be provided in the JSON input."
        )

    return data


def process_cli_args(args: tuple) -> dict:
    """
    Process CLI arguments for Framer configuration.

    Args:
        args (tuple): Tuple of CLI arguments.

    Returns:
        dict: Processed CLI arguments as a dictionary.
    """
    data = {}
    key = None
    for arg in args:
        if arg.startswith("--"):
            key = arg[2:]
        elif key:
            data[key] = arg
            key = None
        else:
            data["prompt"] = arg
            break

    if not data.get("prompt") and not data.get("perception"):
        raise click.UsageError("Either 'prompt' or 'perception' must be provided.")

    return data


@cli.command(help="Run the Text-based User Interface.")
@click.argument("json_input", nargs=-1)
@click.option("--sync", is_flag=True, help="Run in synchronous mode")
@click.option("--stream", is_flag=True, help="Stream the output")
@click.pass_context
def run_framer(ctx, json_input, sync, stream):
    """Run a Framer with the given JSON configuration."""
    try:
        if len(json_input) == 1:
            data = process_json_input(json_input[0])
        else:
            data = process_cli_args(json_input)
    except json.JSONDecodeError:
        raise click.UsageError(
            "Invalid JSON format. Please provide a valid JSON string."
        )

    name = data.get("name", "Default Framer")
    description = data.get("description")
    model = data.get("model", "gpt-3.5-turbo")
    prompt = data.get("prompt")
    perception = data.get("perception")
    soul_seed = data.get("soul_seed")
    max_len = data.get("max_len", 512)

    frame = Frame()
    config = FramedConfig(
        name=name,
        description=description,
        default_model=model,
        soul_seed=soul_seed,
    )

    async def run_async():
        framed = await frame.create_framed(config)
        logger.info(
            f"Running Framer: {name} - {description or 'No description'} with model {model}"
        )

        if framed.soul is None:
            logger.error(
                "Error: Framer's Soul is null. Initializing with default values."
            )
            framed.soul = Soul()

        if perception:
            result = await framed.sense(perception)
        elif prompt:
            result = await framed.prompt(prompt, max_tokens=max_len, stream=stream)
        else:
            logger.error(
                "Error: Neither prompt nor perception provided in the JSON input."
            )
            return

        framed._streamed_response = {"status": "pending", "result": ""}

        if stream:

            async def stream_output():
                while framed._streamed_response["status"] != "finished":
                    new_content = framed._streamed_response["result"]
                    if new_content:
                        click.echo(new_content, nl=False)
                        framed._streamed_response["result"] = ""
                    await asyncio.sleep(0.1)

                # Print any remaining content
                if framed._streamed_response["result"]:
                    click.echo(framed._streamed_response["result"], nl=False)

            await stream_output()
        else:
            click.echo(result)

        logger.info("Framer execution completed")

    asyncio.run(run_async())

    # Log LLM usage metrics
    metrics = frame.get_metrics()
    logger.info("LLM Usage Metrics:")
    logger.info(f"Total calls: {metrics['total_calls']}")
    logger.info(f"Total cost: ${metrics['total_cost']:.4f}")
    for model, data in metrics["models"].items():
        logger.info(f"  {model}: {data['calls']} calls, ${data['cost']:.4f}")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
