"""Tests for context management system."""

import pytest
from pathlib import Path
import tempfile
import shutil

from context import ContextLoader, ProjectContext, PRPRequest, ValidationResult


class TestContextLoader:
    """Test the ContextLoader class."""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory with test files."""
        temp_dir = tempfile.mkdtemp()
        
        # Create test files
        (Path(temp_dir) / "CLAUDE.md").write_text("Test project rules")
        (Path(temp_dir) / "PLANNING.md").write_text("Test planning docs")
        (Path(temp_dir) / "TASK.md").write_text("Test tasks")
        
        # Create examples directory
        examples_dir = Path(temp_dir) / "examples"
        examples_dir.mkdir()
        (examples_dir / "test_example.py").write_text("# Test example code")
        
        # Create PRPs directory
        prps_dir = Path(temp_dir) / "PRPs"
        prps_dir.mkdir()
        (prps_dir / "test_prp.md").write_text("# Test PRP")
        
        yield temp_dir
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_load_project_context(self, temp_project_dir):
        """Test loading complete project context."""
        loader = ContextLoader(temp_project_dir)
        context = loader.load_project_context()
        
        assert isinstance(context, ProjectContext)
        assert context.claude_rules == "Test project rules"
        assert context.planning == "Test planning docs"
        assert context.tasks == "Test tasks"
        assert "test_example.py" in context.examples
        assert "test_prp" in context.prps
    
    def test_context_caching(self, temp_project_dir):
        """Test that context is cached after first load."""
        loader = ContextLoader(temp_project_dir)
        
        # First load
        context1 = loader.load_project_context()
        
        # Modify file
        (Path(temp_project_dir) / "CLAUDE.md").write_text("Modified rules")
        
        # Second load should return cached version
        context2 = loader.load_project_context()
        
        assert context1.claude_rules == context2.claude_rules
        assert context2.claude_rules == "Test project rules"  # Not modified
        
        # Clear cache and reload
        loader.clear_cache()
        context3 = loader.load_project_context()
        assert context3.claude_rules == "Modified rules"
    
    def test_missing_files_handled_gracefully(self, temp_project_dir):
        """Test that missing optional files don't cause errors."""
        # Delete optional files
        (Path(temp_project_dir) / "PLANNING.md").unlink()
        (Path(temp_project_dir) / "TASK.md").unlink()
        
        loader = ContextLoader(temp_project_dir)
        context = loader.load_project_context()
        
        assert context.claude_rules == "Test project rules"
        assert context.planning is None
        assert context.tasks is None
    
    def test_default_claude_rules(self):
        """Test default CLAUDE.md rules when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            loader = ContextLoader(temp_dir)
            context = loader.load_project_context()
            
            assert "Project Awareness" in context.claude_rules
            assert "Code Structure" in context.claude_rules
            assert "Testing" in context.claude_rules


class TestProjectContext:
    """Test the ProjectContext model."""
    
    def test_get_formatted_context(self):
        """Test formatting context for prompts."""
        context = ProjectContext(
            claude_rules="Test rules",
            planning="Test planning",
            tasks="Test tasks",
            examples={"example1.py": "code", "example2.py": "more code"},
            prps={"prp1": "content"}
        )
        
        formatted = context.get_formatted_context()
        
        assert "## Project Rules (CLAUDE.md)" in formatted
        assert "Test rules" in formatted
        assert "## Architecture & Planning" in formatted
        assert "## Current Tasks" in formatted
        assert "## Available Examples" in formatted
        assert "- example1.py" in formatted
        assert "- example2.py" in formatted
    
    def test_formatted_context_with_missing_fields(self):
        """Test formatting when optional fields are missing."""
        context = ProjectContext(
            claude_rules="Test rules",
            planning=None,
            tasks=None
        )
        
        formatted = context.get_formatted_context()
        
        assert "## Project Rules" in formatted
        assert "## Architecture & Planning" not in formatted
        assert "## Current Tasks" not in formatted


class TestValidationResult:
    """Test the ValidationResult model."""
    
    def test_validation_success(self):
        """Test successful validation result."""
        result = ValidationResult(
            success=True,
            errors=[],
            warnings=["Minor warning"]
        )
        
        summary = result.get_summary()
        assert "✅ Validation passed" in summary
    
    def test_validation_failure(self):
        """Test failed validation result."""
        result = ValidationResult(
            success=False,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"]
        )
        
        summary = result.get_summary()
        assert "❌ Validation failed" in summary
        assert "2 errors" in summary
        assert "1 warnings" in summary


class TestPRPRequest:
    """Test the PRPRequest model."""
    
    def test_prp_request_creation(self):
        """Test creating a PRP request."""
        request = PRPRequest(
            feature_description="Add caching system",
            examples=["cache_example.py"],
            documentation_urls=["https://redis.io/docs"],
            considerations="Must support TTL"
        )
        
        assert request.feature_description == "Add caching system"
        assert len(request.examples) == 1
        assert len(request.documentation_urls) == 1
        assert request.considerations == "Must support TTL"
    
    def test_prp_request_defaults(self):
        """Test PRP request with defaults."""
        request = PRPRequest(
            feature_description="Simple feature"
        )
        
        assert request.feature_description == "Simple feature"
        assert request.examples == []
        assert request.documentation_urls == []
        assert request.considerations is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])