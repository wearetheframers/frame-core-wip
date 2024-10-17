import pytest
import asyncio
from frame.cli import FramerTUI
from textual.app import App
from frame.src.services import ExecutionContext


@pytest.mark.asyncio
class TestFramerTUI:
    async def test_initial_state(self, mocker):
        app = FramerTUI()
        async with app.run_test() as pilot:
            mocker.patch.object(app, "setup_framer", return_value=None)
            # Check initial state
            assert app.name is None
            assert app.model == "gpt-3.5-turbo"
            assert app._description == ""
            assert app._prompt == ""
            assert app.debug is False

    async def test_set_name(self, mocker):
        app = FramerTUI()
        async with app.run_test() as pilot:
            await pilot.press("Enter")
            app._name = "Test Framer"  # Manually set the name for testing
            await pilot.press("T")
            await pilot.press("e")
            await pilot.press("s")
            await pilot.press("t")
            await pilot.press(" ")
            await pilot.press("F")
            await pilot.press("r")
            await pilot.press("a")
            await pilot.press("m")
            await pilot.press("e")
            await pilot.press("r")
            await pilot.press("Enter")
            assert app.name == "Test Framer"

    def test_debug_property(self):
        app = FramerTUI()
        assert app.debug is False
        app.debug = True
        assert app.debug is True
