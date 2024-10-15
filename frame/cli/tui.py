import asyncio
import logging
from typing import Dict, Any
from datetime import datetime
import typer
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Input,
    Button,
    Static,
    Label,
    Select,
    Checkbox,
)
from textual.containers import Container, Vertical, ScrollableContainer
from textual import events
import textwrap
from frame.frame import Frame
from frame.src.constants.models import AVAILABLE_MODELS, is_model_supported
from frame.cli.common import (
    logger,
    pretty_log,
    generate_roles_and_goals,
    process_perception_and_log,
    execute_framer,
)


class FramerTUI(App):
    """
    A Text-based User Interface (TUI) for interacting with the Framer.

    This TUI allows users to configure and interact with a Framer instance.
    It provides inputs for the following parameters:

    1. Framer name (optional): A name for the Framer instance.
    2. Model (required): The AI model to be used by the Framer.
    3. Description (optional): A brief description of the Framer's purpose.
    4. Soul seed (optional): A seed phrase to initialize the Framer's "soul" or base personality.
       If left empty, the Framer will start with the default seed "You are a helpful assistant."
    5. Prompt (required): The main input or question for the Framer to respond to.

    The interface also includes options for enabling debug logging and clearing conversation history.
    """

    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_debug", "Toggle Debug")]

    CSS = """
    #response {
        height: 1fr;
        width: 100%;
        border: solid green;
    }
    """

    def __init__(self):
        self._debug = False
        super().__init__()
        # Set up file logging
        file_handler = logging.FileHandler("framer_tui.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        self._name = None
        self._model = AVAILABLE_MODELS[0]
        self._description = ""
        self._prompt = ""
        self._soul_seed = ""
        self._framer = None
        self._expected_output_format_strict = ""
        self._history = []
        self.response = Static(id="response", expand=True)
        self.response_container = ScrollableContainer(self.response)
        self.debug_checkbox = Checkbox("Enable Debug Logging", id="debug_checkbox")

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def name(self):
        return self._name

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def max_len(self):
        return self._max_len

    @property
    def framer(self):
        return self._framer

    @framer.setter
    def framer(self, value):
        self._framer = value

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Vertical(
                Input(
                    placeholder="Enter Framer name (optional, default: Default Framer)",
                    id="name_input",
                ),
                self.response_container,
                Label(id="framer_name_label"),
                Label("Model (required):", id="model_label"),
                Select(
                    [(model, model) for model in AVAILABLE_MODELS],
                    value="gpt-3.5-turbo",
                    id="model_select",
                ),
                Label("Description (optional):", id="description_label"),
                Input(
                    placeholder="Enter Framer description (optional)",
                    id="description_input",
                ),
                Input(
                    placeholder="Enter soul seed (optional)",
                    id="soul_seed_input",
                ),
                self.debug_checkbox,
                Button("Clear History", id="clear_history_button"),
                Label("Debug: Disabled", id="debug_label"),
            ),
            Static("Enter your prompt (required):", id="prompt_label"),
            Input(placeholder="Type your prompt here... (required)", id="prompt_input"),
            Button("Submit", id="submit_button"),
            Static("Conversation History:", id="history_label"),
            Static(id="history_area"),
            id="main_container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up initial UI state when the app is mounted."""
        self.query_one("#name_input").focus()
        self._model = self.query_one("#model_select").value
        self._max_len = 512
        self._debug = False
        self.debug_checkbox.value = self._debug

        self.update_logging()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission event."""
        if event.input.id == "name_input":
            self._name = event.value if event.value else "Default Framer"
            self.query_one("#framer_name_label").update(f"Framer: {self._name}")
            self.query_one("#prompt_input").focus()
            # Set up the Framer after the name is entered
            asyncio.create_task(self.setup_framer())
        elif event.input.id == "description_input":
            self._description = event.value
            self.query_one("#prompt_input").focus()
        elif event.input.id == "soul_seed_input":
            self._soul_seed = event.value
            self.query_one("#prompt_input").focus()
        elif event.input.id == "prompt_input":
            asyncio.create_task(self.submit_prompt())

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle changes in the model selection."""
        if event.select.id == "model_select":
            self.model = event.value
            model_label = self.query_one("Label#model_label")
            model_label.update(f"Model: {self.model}")

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle changes in the debug checkbox."""
        if event.checkbox.id == "debug_checkbox":
            self._debug = event.value
            self.update_logging()

    def update_logging(self) -> None:
        """Update logging based on the debug checkbox state."""
        log_level = logging.DEBUG if self._debug else logging.INFO
        logging.basicConfig(level=log_level)
        logger.setLevel(log_level)
        if self._debug:
            logger.debug("Debug logging enabled")
        else:
            logger.info("Debug logging disabled")

    async def setup_framer(self) -> None:
        """Set up the Framer instance."""
        from frame.src.framer.config import FramerConfig
        from frame.src.framer.framer import Framer
        from frame.frame import Frame

        config = FramerConfig(
            description=self._description,
            name=(
                self._name
                if self._name
                else f"TUI_Framer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ),
            default_model=self._model,
        )

        # Create a Frame instance
        frame = Frame()

        # Use FramerFactory to create the Framer
        from frame.src.framer.framer_factory import FramerFactory

        framer_factory = FramerFactory(config, frame.llm_service)
        self.framer = await framer_factory.create_framer()

        # Set up the soul seed
        self.framer.soul.seed = self._soul_seed

        # Set up the agency
        from frame.src.framer.agency import Agency
        from frame.src.services.context.context_service import Context

        context = Context()
        self.framer.agency = Agency(
            llm_service=frame.llm_service,
            context=context,
            use_local_model=False,
        )

        logger.info(f"Running Framer: {self.framer.config.name}")
        logger.info(f"Using model: {self.framer.config.default_model}")
        logger.info(
            f"Expected output format strict: {self._expected_output_format_strict}"
        )
        logger.info(f"Max length: {self._max_len}")
        logger.info(f"Debug mode: {self._debug}")
        logger.info(f"Soul seed: {self._soul_seed}")
        logger.info(f"Framer roles: {self.framer.agency.roles}")
        logger.info(f"Framer goals: {self.framer.agency.goals}")

        # Update the UI with the current settings
        self.query_one("#framer_name_label").update(f"Framer: {self._name}")
        self.query_one("#model_label").update(f"Model: {self._model}")
        self.query_one("#max_len_label").update(f"Max Length: {self._max_len}")
        self.query_one("#debug_label").update(
            f"Debug: {'Enabled' if self._debug else 'Disabled'}"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press event."""
        if event.button.id == "submit_button":
            asyncio.create_task(self.submit_prompt())
        elif event.button.id == "clear_history_button":
            self.clear_history()

    async def submit_prompt(self) -> None:
        """Submit the prompt and get a response."""
        prompt = self.query_one("#prompt_input").value.strip()
        if not prompt:
            logger.warning("Empty prompt submitted. Ignoring.")
            self.update_response("Error: Empty prompt. Please enter a valid prompt.")
            return

        self._prompt = prompt
        logger.debug(f"Submitting prompt: {prompt}")
        logger.debug(
            f"Current Framer state: name={self._name}, model={self._model}, max_len={self._max_len}"
        )
        self._history.append(f"User: {prompt}")
        self.update_history()

        if not is_model_supported(self._model):
            logger.error(f"Unsupported model: {self._model}")
            self.update_response(
                f"Error: Unsupported model '{self._model}'. Please select a supported model."
            )
            return

        # Ensure Framer is set up before getting a response
        if self.framer is None:
            logger.debug("Framer not initialized. Setting up now.")
            await self.setup_framer()

        # Proceed to get a response if Framer is initialized
        if self.framer is not None:
            await self.get_framer_response(prompt)
        else:
            logger.error("Failed to initialize Framer")
            self.update_response("Error: Failed to initialize Framer")

    async def get_framer_response(self, prompt: str) -> None:
        """Get a response from the Framer and update the UI."""
        self.update_response("Processing...")

        logger.debug(f"Getting Framer response for prompt: {prompt}")

        try:
            # Create a perception from the prompt
            perception_data = {"type": "input", "description": prompt}

            # Use the Framer's sense method to process the perception
            decision = await self.framer.sense(perception_data)

            if decision:
                self.update_response(f"Decision: {decision.action}")
                self.update_response(f"Reasoning: {decision.reasoning}")

                # Process workflows and tasks
                for workflow in self.framer.workflow_manager.workflows:
                    self.update_response(f"Workflow: {workflow.name}")
                    for task in workflow.tasks:
                        self.update_response(f"Task: {task.description}")
                        result = await self.framer.perform_task(task)
                        logger.debug(f"Raw task result: {result}")
                        processed_result = (
                            result.output if hasattr(result, "output") else str(result)
                        )
                        logger.info(f"Task results: {processed_result}")
                        self.update_response(f"- Result: {processed_result}")
            else:
                logger.warning("No decision was made.")
                self.update_response("No decision was made based on the prompt.")

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.exception("Detailed traceback:")
            self.update_response(f"An error occurred: {str(e)}")
        finally:
            self._history.append(f"AI: {self.response.renderable}")
            self.update_history()
            self.update_response("Response received.")

    def update_response(self, text: str) -> None:
        """Update the response area with new text."""
        response = self.query_one("#response", Static)
        if response:
            # Wrap the text to fit within the response widget
            wrapped_text = "\n".join(
                textwrap.wrap(text, width=self.response.size.width - 2)
            )
            response.update(wrapped_text)
            logger.info(f"Updated response: {text}")
            self.update_history()
        else:
            logger.warning("Response element not found. Creating it.")
            new_response = Static(text, id="response", expand=True)
            self.mount(new_response)

    def update_history(self) -> None:
        """Update the conversation history display."""
        history_area = self.query_one("#history_area")
        history_text = "\n\n".join(self._history[-5:])  # Show last 5 interactions
        history_area.update(history_text)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history = []
        self.update_history()

    def action_toggle_debug(self) -> None:
        """Toggle debug mode."""
        self._debug = not self._debug
        self.debug_checkbox.value = self._debug
        self.update_logging()


def run_tui():
    """Run the TUI application."""
    print("Starting FramerTUI...")
    try:
        app = FramerTUI()
        app.run()
    except Exception as e:
        print(f"Error running FramerTUI: {e}")
        import traceback

        traceback.print_exc()
