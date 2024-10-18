import pytest
from unittest.mock import Mock, patch
from frame.src.plugins.search_extract_summarize_plugin import (
    SearchExtractSummarizePlugin,
)


@pytest.fixture
def mock_framer():
    return Mock()


@pytest.fixture
def plugin(mock_framer):
    return SearchExtractSummarizePlugin(mock_framer)


def test_plugin_initialization(plugin):
    assert plugin.framer is not None
    assert plugin.logger is not None


@patch("frame.src.plugins.search_extract_summarize_plugin.requests")
@patch("frame.src.plugins.search_extract_summarize_plugin.BeautifulSoup")
@patch("frame.src.plugins.search_extract_summarize_plugin.OpenAI")
def test_search_extract_summarize(mock_openai, mock_bs, mock_requests, plugin):
    # Mock the necessary components
    mock_requests.get.return_value.json.return_value = {
        "results": [{"link": "http://example.com"}]
    }
    mock_bs.return_value.get_text.return_value = "Sample text"
    mock_openai.return_value.chat.completions.create.return_value.choices[
        0
    ].message.content = "Summarized content"

    # Call the method
    result = plugin.search_extract_summarize("test query")

    # Assert the result
    assert "Summarized content" in result
    assert "http://example.com" in result


@pytest.mark.parametrize(
    "query,expected",
    [
        ("python programming", "python+programming"),
        ("AI & ML", "AI+%26+ML"),
    ],
)
def test_search_web(query, expected, plugin):
    with patch(
        "frame.src.plugins.search_extract_summarize_plugin.requests"
    ) as mock_requests:
        mock_requests.get.return_value.json.return_value = {"results": []}
        plugin.search_web(query, None, None)
        called_url = mock_requests.get.call_args[0][0]
        assert expected in called_url


def test_chunk_results(plugin):
    content = "This is a test content for chunking."
    result = plugin.chunk_results({"http://example.com": content}, 10, 2)
    assert len(result["http://example.com"]) == 3
    assert result["http://example.com"][0] == "This is a "
    assert result["http://example.com"][1] == "a test co"
    assert result["http://example.com"][2] == "content fo"


# Add more tests for other methods as needed
