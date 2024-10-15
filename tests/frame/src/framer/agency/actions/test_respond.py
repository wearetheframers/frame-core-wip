import pytest
from unittest.mock import Mock
from frame.src.framer.agency.actions.respond import respond
from frame.src.framer.agency.execution_context import ExecutionContext

@pytest.fixture
def mock_framer():
    return Mock()

def test_respond(mock_framer):
    input_data = "Hello, how are you?"
    result = respond(mock_framer, input_data)
    assert result == f"Response to input: {input_data}"
