import pytest
from click.testing import CliRunner
from unittest.mock import AsyncMock, Mock
from frame.frame import Frame
from frame.src.services.llm.main import LLMService
from frame.cli import cli as cli_app
from frame.frame import Frame
import re
from frame.src.framer.agency.agency import Agency
from frame.src.framer.agency.execution_context import ExecutionContext


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_help(runner):
    result = runner.invoke(cli_app, ["--help"])
    assert result.exit_code == 0
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in result.output


def test_cli_tui_command(runner, mocker):
    mock_framer_tui = mocker.patch("frame.cli.tui.FramerTUI")
    mock_framer_tui_instance = mock_framer_tui.return_value
    result = runner.invoke(cli_app, ["tui"])
    assert result.exit_code == 0
    mock_framer_tui.assert_called_once()
    mock_framer_tui_instance.run.assert_called_once()


def test_cli_run_framer_command(runner, mocker):
    mock_logger = mocker.patch("frame.cli.cli.logger")
    mock_execute_framer = mocker.patch(
        "frame.cli.cli.execute_framer", return_value={"result": "success"}
    )
    mock_frame = mocker.patch("frame.frame.Frame", autospec=True)
    mock_llm_service = mocker.patch(
        "frame.src.services.llm.main.LLMService", autospec=True
    )
    mock_frame_instance = mock_frame.return_value
    mock_frame_instance.llm_service = mock_llm_service.return_value
    mock_frame_instance.get_metrics.return_value = {
        "total_calls": 1,
        "total_cost": 0.001,
    }

    result = runner.invoke(
        cli_app,
        ["run-framer", "--prompt", "Test prompt", "--name", "Test Framer"],
        catch_exceptions=False,
    )

    assert (
        result.exit_code == 0
    ), f"Exit code was {result.exit_code}, expected 0. Output: {strip_ansi_codes(result.output)}"

    # Check if Frame constructor was called
    mock_frame.assert_called_once()

    # Check if execute_framer was called
    assert mock_execute_framer.call_count > 0, "execute_framer was not called"

    # Check if the completion message is in the logger output
    mock_logger.info.assert_any_call(
        "Framer execution completed. Result: {'result': 'success'}"
    )

    # Check if the execute_framer function was called with the correct arguments
    call_args = mock_execute_framer.call_args
    assert call_args is not None, "execute_framer was not called"
    args, kwargs = call_args
    assert isinstance(
        args[0], type(mock_frame.return_value)
    ), f"First argument is not a Frame instance, it's {type(args[0])}"
    assert args[1] == {
        "name": "Test Framer",
        "prompt": "Test prompt",
        "model": "gpt-4o-mini",
    }
    assert args[2] is False  # sync flag
    assert args[3] is False  # stream flag


def strip_ansi_codes(text):
    ansi_escape = re.compile(r"\x1b\[([0-9]+)(;[0-9]+)*m")
    return ansi_escape.sub("", text)


def test_cli_run_framer_with_prompt(runner, mocker):
    mock_logger = mocker.patch("frame.cli.cli.logger")
    mock_execute_framer = mocker.patch(
        "frame.cli.cli.execute_framer", return_value={"result": "success"}
    )
    mock_frame = mocker.patch("frame.frame.Frame", autospec=True)
    mock_frame_instance = mock_frame.return_value
    mock_frame_instance.llm_service = mocker.Mock(spec=LLMService)
    mock_frame_instance.llm_service.get_completion.return_value = '{"action": "think", "parameters": {"thought": "Test thought"}, "reasoning": "Test reasoning", "confidence": 0.9, "priority": 5}'
    mock_execute_framer.return_value = {"result": "success"}
    mock_click_echo = mocker.patch("frame.cli.cli.click.echo")

    result = runner.invoke(
        cli_app, ["run-framer", "--name", "Test Framer", "--prompt", "Test prompt"]
    )

    assert (
        result.exit_code == 0
    ), f"Exit code was {result.exit_code}, expected 0. Output: {strip_ansi_codes(str(result.output))}"

    # Ensure the output is a string before formatting
    output = strip_ansi_codes(str(result.output))
    assert isinstance(output, str), "Output is not a string"

    # Check if execute_framer was called
    mock_execute_framer.assert_called_once()

    # Check if Frame constructor was called
    mock_frame.assert_called_once()

    # Check if execute_framer was called
    mock_execute_framer.assert_called_once()

    # Check if the execute_framer function was called with the correct arguments
    call_args = mock_execute_framer.call_args
    assert call_args is not None, "execute_framer was not called"
    args, kwargs = call_args
    assert isinstance(
        args[0], type(mock_frame.return_value)
    )  # Check if the first argument is a Frame instance
    assert args[1]["name"] == "Test Framer"
    assert args[1]["prompt"] == "Test prompt"
    assert args[2] is False  # sync flag
    assert args[3] is False  # stream flag

    # Check if the completion message is in the logger output
    mock_logger.info.assert_any_call(
        "Framer execution completed. Result: {'result': 'success'}"
    )
    assert mock_click_echo.call_count >= 1
    mock_click_echo.assert_any_call("Framer execution completed")


def test_agency_creation(mocker):
    mock_llm_service = mocker.Mock()
    mock_context = mocker.Mock()
    agency = Agency(llm_service=mock_llm_service, context=mock_context)
    assert isinstance(agency, Agency)
    assert agency.llm_service == mock_llm_service
    assert agency.context == mock_context
