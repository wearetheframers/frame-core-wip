import click
import sys
import os
import logging
import asyncio
import atexit

import json
from frame.src.framer.config import FramerConfig
from frame.src.framer.framer_factory import FramerFactory
from frame.src.framer.agency import Agency
from frame.src.services.context.context_service import Context
from frame.cli.common import process_perception_and_log

from frame.src.utils.cleanup import cleanup

# Initialize colorama
from colorama import init

init(autoreset=True)

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from frame.cli.common import pretty_log
from frame.src.constants.models import DEFAULT_MODEL
from frame.src.framer.brain.perception import Perception
from frame.sync_frame import sync_frame

# Set up logging
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@click.group()
@click.option("--openai-api-key", envvar="OPENAI_API_KEY", help="OpenAI API key")
@click.option("--mistral-api-key", envvar="MISTRAL_API_KEY", help="Mistral API key")
@click.option(
    "--huggingface-api-key", envvar="HUGGINGFACE_API_KEY", help="Hugging Face API key"
)
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--expected-output-format-strict",
    help="Specify the exact type of value to be generated",
)
@click.option("--default-model", help="Set the default model for all operations")
@click.pass_context
def cli(
    # Main entry point for the CLI application.
    ctx,
    openai_api_key,
    mistral_api_key,
    huggingface_api_key,
    debug,
    default_model,
    expected_output_format_strict,
):
    # Register cleanup function
    atexit.register(cleanup)
    """
    Frame CLI for quick testing and interaction.

    This function sets up the CLI context and initializes logging based on
    the provided options.

    Args:
        ctx (Context): Click context object for managing command-line options.
        openai_api_key (str): OpenAI API key for accessing OpenAI services.
        mistral_api_key (str): Mistral API key for accessing Mistral services.
        huggingface_api_key (str): Hugging Face API key for accessing Hugging Face services.
        debug (bool): Flag to enable or disable debug logging.
        default_model (str): Default model to use for operations.
    """
    ctx.ensure_object(dict)
    ctx.obj["openai_api_key"] = openai_api_key
    ctx.obj["mistral_api_key"] = mistral_api_key
    ctx.obj["huggingface_api_key"] = huggingface_api_key
    ctx.obj["default_model"] = default_model

    ctx.obj["expected_output_format_strict"] = expected_output_format_strict

    if debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        logging.getLogger().setLevel(logging.INFO)


def execute_framer(frame, data, sync, stream):
    """
    Execute the Framer based on the provided configuration.

    This function sets up the Framer configuration and executes it in either
    synchronous or asynchronous mode.

    Args:
        frame (Frame): Frame instance for managing Framer operations.
        data (dict): Configuration data for the Framer.
        sync (bool): Flag to run in synchronous mode.
        stream (bool): Flag to enable streaming output.

    Returns:
        Any: Result of the Framer execution.
    """
    import json
    from frame.src.framer.config import FramerConfig

    logger.debug("execute_framer function started")

    name = data.get("name", "Default Framer")
    description = data.get("description")
    model = data.get("model", DEFAULT_MODEL).lower()
    prompt = data.get("prompt")
    perception = data.get("perception")
    soul_seed = data.get("soul_seed", "default_soul_seed")
    max_len = data.get("max_len", 512)

    logger.debug(
        f"Framer configuration: name={name}, description={description}, model={model}"
    )
    logger.debug(f"Soul seed: {soul_seed}")
    logger.debug(f"Prompt: {prompt}")
    logger.debug(f"Perception: {perception}")
    logger.debug(f"Max length: {max_len}")

    if not prompt and not perception:
        logger.error("Neither prompt nor perception provided in the JSON input")
        raise click.UsageError(
            "Either 'prompt' or 'perception' must be provided in the JSON input."
        )

    config = FramerConfig(
        name=name,
        description=description,
        default_model=model,
    )
    logger.debug(f"FramerConfig created: {config}")

    try:
        if sync:
            logger.debug("Executing in synchronous mode")
            result = sync_execute_framer(frame, config, prompt, perception, max_len)
        else:
            logger.debug("Executing in asynchronous mode")
            framer = asyncio.run(
                run_async(
                    frame,
                    name,
                    description,
                    model,
                    prompt,
                    perception,
                    soul_seed,
                    max_len,
                    stream,
                )
            )
        logger.debug(f"Execution completed. Result: {framer}")
        if stream:

            async def wait_for_streaming():
                last_position = 0
                while framer._streamed_response["status"] != "finished":
                    new_text = framer._streamed_response["result"][last_position:]
                    if new_text:
                        print(new_text, end="", flush=True)
                        last_position += len(new_text)
                    await asyncio.sleep(0.1)  # Wait for streaming to complete
                # Print any remaining text after status is finished
                new_text = framer._streamed_response["result"][last_position:]
                if new_text:
                    print(new_text, end="", flush=True)
                return framer._streamed_response["result"]

            return asyncio.run(wait_for_streaming())
        else:
            return result
    except Exception as e:
        logger.error(f"An error occurred during framer execution: {str(e)}")
        logger.exception("Exception details:")
        raise


@cli.command()
def tui():
    """Run the Text-based User Interface."""
    from frame.cli.tui import run_tui

    run_tui()


@cli.command()
@click.option("--prompt", help="Prompt for the Framer")
@click.option("--name", default="Default Framer", help="Name of the Framer")
@click.option("--model", default="gpt-4o-mini", help="Model to use for the Framer")
@click.option("--debug/--no-debug", default=False, help="Enable debug logging")
@click.option("--sync", is_flag=True, help="Run in synchronous mode")
@click.option("--stream", is_flag=True, help="Stream the output")
@click.pass_context
def run_framer(ctx, prompt, name, model, debug, sync, stream):
    """Run a Framer with the given configuration."""
    from frame.frame import Frame

    if debug:
        logger.setLevel(logging.DEBUG)

    logger.debug(f"Debug flag: {debug}")
    logger.debug(f"Sync flag: {sync}")
    logger.debug(f"Stream flag: {stream}")
    logger.debug(f"Name: {name}")
    logger.debug(f"Model: {model}")
    logger.debug(f"Prompt: {prompt}")

    data = {"name": name, "model": model, "prompt": prompt}

    logger.debug(f"Final parsed data: {data}")

    frame = Frame(
        openai_api_key=ctx.obj.get("openai_api_key"),
        mistral_api_key=ctx.obj.get("mistral_api_key"),
        huggingface_api_key=ctx.obj.get("huggingface_api_key"),
        default_model=model,
    )
    from frame.src.constants.api_keys import HUGGINGFACE_API_KEY
    if not HUGGINGFACE_API_KEY:
        logger.warning("Hugging Face API key is not set. Some features may not work.")

    result = execute_framer(frame, data, sync, stream)
    logger.info(f"Framer execution completed. Result: {result}")

    # Log LLM usage metrics
    metrics = frame.get_metrics()
    logger.info("LLM Usage Metrics:")
    logger.info(f"Total calls: {metrics.get('total_calls', 0)}")
    logger.info(f"Total cost: ${metrics.get('total_cost', 0):.4f}")
    for model, model_data in metrics.get("models", {}).items():
        logger.info(
            f"  {model}: {model_data.get('calls', 0)} calls, ${model_data.get('cost', 0):.4f}"
        )


def execute_framer(frame, data, sync, stream):
    """Execute the Framer based on the provided configuration."""
    name = data.get("name", "Default Framer")
    description = data.get("description")
    model = data.get("model", "gpt-3.5-turbo").lower()
    prompt = data.get("prompt")
    perception = data.get("perception")
    soul_seed = data.get("soul_seed", "You are a helpful AI")
    max_len = data.get("max_len", 512)

    logger.debug(f"Soul seed: {soul_seed}")

    if not prompt and not perception:
        raise click.UsageError(
            "Either 'prompt' or 'perception' must be provided in the JSON input."
        )

    config = FramerConfig(
        name=name,
        description=description,
        default_model=model,
    )

    if sync:
        return sync_execute_framer(frame, config, prompt, perception, max_len)
    else:
        return asyncio.run(
            run_async(
                frame,
                name,
                description,
                model,
                prompt,
                perception,
                soul_seed,
                max_len,
                stream,
            )
        )


def sync_execute_framer(frame, config, prompt, perception, max_len):
    framer = asyncio.run(sync_frame.create_framer(config=config))
    logger.info(f"Running Framer (Sync): {config.name}")
    logger.info(f"Using model: {config.default_model}")
    logger.debug(f"Prompt: {prompt}")
    roles = pretty_log(framer.agency.roles)
    goals = pretty_log(framer.agency.goals)
    if roles:
        logger.info(f"Framer roles: {roles}")
    if goals:
        logger.info(f"Framer goals: {goals}")

    if perception:
        decision = sync_frame.process_perception(framer, perception)
        logger.info(f"Perception processed. Decision: {decision}")

    if prompt:
        perception_data = {"type": "hearing", "data": {"text": prompt}}
        # Assuming the correct method is process_perception
        decision = sync_frame.process_perception(framer, perception_data)
        logger.info(f"Perception processed. Decision: {decision}")
        tasks = sync_frame.generate_tasks_from_perception(
            framer, perception_data, max_len=max_len
        )
        logger.info(f"Generated tasks: {pretty_log(tasks)}")
        if isinstance(tasks, dict) and "tasks" in tasks:
            for task in tasks["tasks"]:
                result = sync_frame.perform_task(framer, task)
                logger.debug(f"Raw task result: {pretty_log(result)}")
                logger.info(f"Task '{task['description']}' result: {result}")
        else:
            logger.warning(
                "No tasks generated from the prompt or unexpected task format."
            )

    return framer


@cli.command()
@click.argument("json_input", nargs=-1)
@click.option("--debug/--no-debug", default=False, help="Enable debug logging")
@click.option("--sync", is_flag=True, help="Run in synchronous mode")
@click.option("--stream", is_flag=True, help="Stream the output")
@click.pass_context
def run_framer_json(ctx, json_input, debug, sync, stream):
    """Run a Framer with the given JSON configuration."""
    import json
    from frame.frame import Frame

    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug("run_framer command started")

    logger.debug(f"Debug flag: {debug}")
    logger.debug(f"Sync flag: {sync}")
    logger.debug(f"Stream flag: {stream}")
    logger.debug(f"Raw JSON input: {json_input}")

    # Join all parts of json_input into a single string
    json_string = " ".join(json_input)
    logger.debug(f"Joined JSON input: {json_string}")

    # Remove any leading/trailing quotes and spaces
    json_string = json_string.strip("'\" ")
    logger.debug(f"Stripped JSON input: {json_string}")

    # Check if the input is a valid JSON
    try:
        data = json.loads(json_string)
        logger.debug(f"Parsed JSON data: {data}")
    except json.JSONDecodeError:
        # If not a valid JSON, treat the entire input as a prompt
        logger.debug("Input is not a valid JSON. Treating as a prompt.")
        data = {"prompt": json_string.strip("'\" ")}

    logger.debug(f"Final parsed data: {data}")

    logger.debug("Creating Frame instance")
    frame = Frame(
        openai_api_key=ctx.obj.get("openai_api_key"),
        mistral_api_key=ctx.obj.get("mistral_api_key"),
        huggingface_api_key=ctx.obj.get("huggingface_api_key"),
        default_model=ctx.obj.get("default_model"),
    )

    try:
        logger.debug("Executing framer")
        result = execute_framer(frame, data, sync, stream)
        logger.info(f"Framer execution completed. Result: {result}")
    except Exception as e:
        logger.error(f"An error occurred during framer execution: {str(e)}")
        logger.exception("Exception details:")

    logger.debug("run_framer command finished")
    # Log LLM usage metrics
    metrics = frame.get_metrics()
    logger.info("LLM Usage Metrics:")
    logger.info(f"Total calls: {metrics['total_calls']}")
    logger.info(f"Total cost: ${metrics['total_cost']:.4f}")
    for model, data in metrics["models"].items():
        logger.info(f"  {model}: {data['calls']} calls, ${data['cost']:.4f}")


async def run_async(
    frame, name, description, model, prompt, perception, soul_seed, max_len, stream
):
    """
    Run the Framer asynchronously.
    """
    logger.debug(f"run_async - Soul seed: {soul_seed}")
    config = FramerConfig(
        name=name,
        description=description,
        default_model=model,
    )
    framer_factory = FramerFactory(config, frame.llm_service)
    framer = await framer_factory.create_framer()
    context = Context()  # Create a new Context
    framer.agency = Agency(
        llm_service=frame.llm_service,
        context=context,
    )
    logger.info(f"Using model: {framer.config.default_model}")
    logger.debug(f"Prompt: {prompt}")

    try:
        logger.debug(f"Framer agency before generate_roles_and_goals: {framer.agency}")
        roles, goals = await framer.agency.generate_roles_and_goals()
        framer.agency.set_roles(roles)
        framer.agency.set_goals(goals)
        logger.debug(f"Framer agency after generate_roles_and_goals: {framer.agency}")
        logger.info(f"Generated roles: {roles}")
        logger.info(f"Generated goals: {goals}")

        if isinstance(perception, str):
            perception_data = json.loads(perception)
        elif isinstance(perception, dict):
            perception_data = perception
        elif prompt:
            perception_data = {"type": "input", "data": {"text": prompt}}
        else:
            raise click.UsageError("Either prompt or perception must be provided.")

        if isinstance(perception_data, dict):
            if "data" in perception_data:
                perception = Perception.from_dict(perception_data)
            else:
                logger.error("Perception data is missing the 'data' key.")
                raise ValueError(
                    "Perception data must include a 'data' key with a dictionary value."
                )
        else:
            perception = perception_data
        decision = await framer.sense(perception)
        if decision:
            # Log the summary
            logger.info("Execution Summary:")
            total_workflows = len(framer.workflow_manager.workflows)
            total_tasks = sum(
                len(workflow.tasks) for workflow in framer.workflow_manager.workflows
            )
            logger.info(f"Total Workflows created: {total_workflows}")
            logger.info(f"Total Tasks created: {total_tasks}")
            for workflow in framer.workflow_manager.workflows:
                logger.info(f"Workflow has {len(workflow.tasks)} tasks.")
                for task in workflow.tasks:
                    logger.info(
                        f"Task Name: {task.description}, Task Priority: {task.priority}"
                    )
                    # Execute each task and log the result
                    task_result = await framer.agency.execute_task(task)
                    logger.info(
                        f"Executed Task '{task.description}' Result: {task_result}"
                    )
            logger.info(f"Decision reasoning: {decision.reasoning}")
            # _roles = pretty_log(framer.agency.get_roles())
            # _goals = pretty_log(framer.agency.get_goals())
            _roles = framer.agency.get_roles()
            _goals = framer.agency.get_goals()
            for role in _roles:
                if role not in _roles:
                    logger.info(f"Updated role: {role}")
            for goal in _goals:
                if goal not in _goals:
                    logger.info(f"Updated goal: {goal}")
            logger.info(f"Decision: {pretty_log(decision)}")
        return framer
    except AttributeError as e:
        logger.error(f"An error occurred: {e}")
        logger.error("Make sure the Framer class has a process_perception method.")
        logger.exception("Detailed traceback:")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.exception("Detailed traceback:")


async def stream_output(framer, prompt):
    """Stream the output from a Framer."""
    async for chunk in framer.stream_completion(prompt):
        print(chunk, end="", flush=True)
    print()  # Print a newline at the end


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
