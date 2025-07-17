"""Testing patterns for Make It Heavy."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

# Pattern 1: Basic unit test structure
def test_basic_functionality():
    """Test happy path for a function."""
    # Arrange
    from tools.calculator_tool import CalculatorTool
    tool = CalculatorTool({})
    
    # Act
    result = tool.execute(expression="2 + 2")
    
    # Assert
    assert result["status"] == "success"
    assert result["result"] == 4

# Pattern 2: Testing with fixtures
@pytest.fixture
def mock_agent():
    """Fixture for creating a mock agent."""
    agent = Mock()
    agent.run.return_value = "Mock response"
    agent.config = {"model": "test-model"}
    return agent

@pytest.fixture
def sample_config():
    """Fixture for test configuration."""
    return {
        "openrouter": {
            "api_key": "test-key",
            "base_url": "https://test.api",
            "model": "test-model"
        },
        "system_prompt": "Test prompt"
    }

def test_with_fixtures(mock_agent, sample_config):
    """Demonstrate using fixtures in tests."""
    # Use fixtures
    assert mock_agent.config["model"] == "test-model"
    assert sample_config["openrouter"]["api_key"] == "test-key"

# Pattern 3: Testing error cases
def test_error_handling():
    """Test that errors are handled properly."""
    from tools.read_file_tool import ReadFileTool
    tool = ReadFileTool({})
    
    # Test non-existent file
    result = tool.execute(path="/non/existent/file.txt")
    
    assert result["status"] == "error"
    assert "not found" in result["error"].lower()

# Pattern 4: Testing with mocks
@patch('requests.get')
def test_api_call_with_mock(mock_get):
    """Test external API calls using mocks."""
    from tools.search_tool import SearchTool
    
    # Configure mock
    mock_response = Mock()
    mock_response.json.return_value = {"results": ["item1", "item2"]}
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    # Test
    tool = SearchTool({"search": {"max_results": 5}})
    result = tool.execute(query="test query")
    
    # Verify
    assert mock_get.called
    assert result["status"] == "success"

# Pattern 5: Parametrized tests
@pytest.mark.parametrize("expression,expected", [
    ("2 + 2", 4),
    ("10 - 5", 5),
    ("3 * 4", 12),
    ("15 / 3", 5),
    ("2 ** 3", 8),
])
def test_calculator_operations(expression, expected):
    """Test multiple calculator operations."""
    from tools.calculator_tool import CalculatorTool
    tool = CalculatorTool({})
    
    result = tool.execute(expression=expression)
    
    assert result["status"] == "success"
    assert result["result"] == expected

# Pattern 6: Testing async code (wrapped in sync)
def test_async_wrapped_operation():
    """Test async operations wrapped in sync context."""
    import asyncio
    
    async def async_operation():
        await asyncio.sleep(0.1)
        return {"status": "success", "data": "async result"}
    
    # Run async in sync context
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(async_operation())
    loop.close()
    
    assert result["status"] == "success"
    assert result["data"] == "async result"

# Pattern 7: Testing with context managers
def test_file_operations_with_context():
    """Test file operations using context managers."""
    from pathlib import Path
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tf:
        tf.write("Test content")
        temp_path = tf.name
    
    try:
        # Test reading the file
        from tools.read_file_tool import ReadFileTool
        tool = ReadFileTool({})
        result = tool.execute(path=temp_path)
        
        assert result["status"] == "success"
        assert result["content"] == "Test content"
        
    finally:
        # Cleanup
        Path(temp_path).unlink()

# Pattern 8: Testing class initialization
def test_agent_initialization():
    """Test proper initialization of complex classes."""
    from agent import OpenRouterAgent
    import yaml
    
    with patch('builtins.open', mock_open(read_data=yaml.dump({
        "openrouter": {"api_key": "test", "base_url": "http://test"},
        "system_prompt": "Test"
    }))):
        agent = OpenRouterAgent(config_path="test.yaml", context_aware=False)
        
        assert agent.config is not None
        assert agent.silent is False
        assert hasattr(agent, 'client')
        assert hasattr(agent, 'tools')

# Pattern 9: Testing with side effects
def test_retry_logic_with_side_effects():
    """Test retry logic with different responses."""
    from tools.search_tool import SearchTool
    
    with patch('requests.get') as mock_get:
        # First call fails, second succeeds
        mock_get.side_effect = [
            Exception("Network error"),
            Mock(status_code=200, json=lambda: {"results": []})
        ]
        
        tool = SearchTool({})
        # Tool should retry and succeed
        tool.execute(query="test")
        
        assert mock_get.call_count >= 2
        # Result depends on tool's retry implementation

# Pattern 10: Integration test pattern
def test_agent_tool_integration():
    """Test agent using tools in realistic scenario."""
    from agent import OpenRouterAgent
    
    # Mock the entire LLM interaction
    with patch.object(OpenRouterAgent, 'call_llm') as mock_llm:
        # Configure mock response
        mock_response = Mock()
        mock_response.choices = [Mock(
            message=Mock(
                content="Test response",
                tool_calls=None
            ),
            finish_reason="stop"
        )]
        mock_llm.return_value = mock_response
        
        # Test
        agent = OpenRouterAgent(context_aware=False)
        result = agent.run("Test query")
        
        assert "Test response" in result

# Helper function for test data
def create_test_data(data_type: str) -> Dict[str, Any]:
    """Create consistent test data for various tests."""
    test_data = {
        "agent_response": {
            "status": "success",
            "message": "Operation completed",
            "data": {"key": "value"}
        },
        "tool_result": {
            "status": "success",
            "result": "Tool executed successfully"
        },
        "error_response": {
            "status": "error",
            "error": "Test error message"
        }
    }
    return test_data.get(data_type, {})

# Mock helper for consistent mocking
def mock_open(read_data=''):
    """Helper to mock file operations."""
    import io
    m = MagicMock(spec=io.IOBase)
    handle = MagicMock(spec=io.TextIOWrapper)
    handle.read.return_value = read_data
    handle.__enter__.return_value = handle
    m.return_value = handle
    return m

# Anti-patterns to avoid in tests
def test_anti_patterns():
    """Examples of what NOT to do in tests."""
    
    # ❌ Don't test implementation details
    # def test_private_method():
    #     obj._private_method()  # Testing internals
    
    # ❌ Don't write tests without assertions
    # def test_something():
    #     result = function()
    #     # No assert!
    
    # ❌ Don't use real external services
    # def test_api():
    #     response = requests.get("https://real-api.com")
    #     # Should mock this!
    
    # ❌ Don't ignore test isolation
    # global_state = []
    # def test_one():
    #     global_state.append(1)  # Modifies global
    # def test_two():
    #     assert len(global_state) == 0  # Fails!
    
    pass

if __name__ == "__main__":
    # Run a simple test
    print("Running example test...")
    test_basic_functionality()
    print("✅ Test passed!")
    
    # Show parametrized test data
    print("\nParametrized test examples:")
    for expr, expected in [("2 + 2", 4), ("10 - 5", 5)]:
        print(f"  {expr} = {expected}")