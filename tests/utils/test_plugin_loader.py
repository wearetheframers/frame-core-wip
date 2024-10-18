import pytest
from unittest.mock import patch, MagicMock
from frame.src.utils.plugin_loader import load_plugins, load_plugin_config
from frame.src.framer.brain.plugins import PluginBase

class MockPlugin(PluginBase):
    def __init__(self, config):
        super().__init__(config)
        self.actions = {
            "test_action": self.test_action
        }

    def test_action(self):
        return "Test action executed"

    def get_actions(self):
        return self.actions

@pytest.fixture
def mock_plugin_dir(tmp_path):
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    return str(plugin_dir)

def test_load_plugins(mock_plugin_dir):
    with patch('frame.src.utils.plugin_loader.importlib.import_module') as mock_import, \
         patch('frame.src.utils.plugin_loader.os.listdir') as mock_listdir, \
         patch('frame.src.utils.plugin_loader.os.path.isdir') as mock_isdir:
        mock_module = MagicMock()
        mock_module.MockPlugin = MockPlugin
        mock_import.return_value = mock_module
        mock_listdir.return_value = ['mock_plugin']
        mock_isdir.return_value = True

        plugins, warnings = load_plugins(mock_plugin_dir)

        assert len(plugins) == 1
        assert "mock_plugin" in plugins
        assert isinstance(plugins["mock_plugin"], MockPlugin)
        assert len(warnings) == 0

def test_load_plugins_with_conflict(mock_plugin_dir):
    with patch('frame.src.utils.plugin_loader.importlib.import_module') as mock_import, \
         patch('frame.src.utils.plugin_loader.os.listdir') as mock_listdir, \
         patch('frame.src.utils.plugin_loader.os.path.isdir') as mock_isdir:
        mock_module1 = MagicMock()
        mock_module1.MockPlugin1 = MockPlugin
        mock_module2 = MagicMock()
        mock_module2.MockPlugin2 = MockPlugin
        mock_import.side_effect = [mock_module1, mock_module2]
        mock_listdir.return_value = ['mock_plugin1', 'mock_plugin2']
        mock_isdir.return_value = True

        plugins, warnings = load_plugins(mock_plugin_dir)

        assert len(plugins) == 2
        assert "mock_plugin1" in plugins
        assert "mock_plugin2" in plugins
        assert len(warnings) == 1
        assert "conflicts with an existing action" in warnings[0]

def test_load_plugin_config(mock_plugin_dir, monkeypatch):
    config_file = os.path.join(mock_plugin_dir, "config.json")
    with open(config_file, 'w') as f:
        f.write('{"test_key": "test_value"}')

    monkeypatch.setenv("TEST_KEY", "env_value")

    config = load_plugin_config(mock_plugin_dir)

    assert config["test_key"] == "env_value"

def test_load_plugin_config_no_file(mock_plugin_dir):
    config = load_plugin_config(mock_plugin_dir)

    assert config == {}
