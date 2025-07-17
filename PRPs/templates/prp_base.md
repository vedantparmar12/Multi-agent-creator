name: "Base PRP Template - Make It Heavy Context Engineering"
description: |

## Purpose
Template optimized for AI agents to implement features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
[What needs to be built - be specific about the end state and desires]

## Why
- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What
[User-visible behavior and technical requirements]

### Success Criteria
- [ ] [Specific measurable outcomes]

## All Needed Context

### Documentation & References (list all context needed to implement the feature)
```yaml
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]
  
- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]
  
- doc: [Library documentation URL] 
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]

- docfile: [PRPs/ai_docs/file.md]
  why: [docs that the user has pasted in to the project]

```

### Current Codebase Structure
```bash
# Output of tree or find command showing relevant files
```

### Desired Codebase Structure
```bash
# Structure after implementation with new files noted
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: [Library name] requires [specific setup]
# Example: OpenRouter has rate limits - implement exponential backoff
# Example: Tool discovery happens at import time - restart required
```

## Implementation Blueprint

### Data Models and Structure

```python
# Core data models needed for the feature
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ExampleModel(BaseModel):
    """Description of model purpose"""
    field: str = Field(description="What this field does")
```

### List of Tasks

```yaml
Task 1: [Task Name]
CREATE/MODIFY path/to/file.py:
  - PATTERN: Follow existing patterns from similar_file.py
  - IMPLEMENT: Core functionality
  - VALIDATE: Include error handling

Task 2: [Task Name]
CREATE tests/test_feature.py:
  - PATTERN: Mirror test structure from test_agent.py
  - TEST: Happy path, edge cases, error scenarios
  - VALIDATE: 100% coverage for new code

[Additional tasks...]
```

### Per-Task Pseudocode

```python
# Task 1: [Implementation details]
def new_feature(param: str) -> Result:
    # PATTERN: Always validate input first
    validated = validate_input(param)
    
    # CRITICAL: Handle rate limits for external APIs
    with rate_limiter:
        result = await api_call(validated)
    
    # PATTERN: Use consistent error handling
    return format_response(result)
```

### Integration Points
```yaml
CONFIG:
  - add to: config.yaml
  - section: "feature_config"
  - pattern: "feature_enabled: true"
  
TOOLS:
  - add to: tools/
  - pattern: "Inherit from BaseTool"
  
TESTS:
  - add to: tests/
  - pattern: "Use pytest fixtures"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check . --fix              # Auto-fix style issues
mypy path/to/file.py           # Type checking

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# tests/test_feature.py
def test_happy_path():
    """Basic functionality works"""
    result = feature.process("valid_input")
    assert result.success

def test_error_handling():
    """Handles errors gracefully"""
    with pytest.raises(ValidationError):
        feature.process("invalid")
```

```bash
# Run and iterate until passing:
pytest tests/test_feature.py -v
```

### Level 3: Integration Test
```bash
# Test with single agent
python main.py
# Input: "Test the new feature"
# Expected: Feature works correctly

# Test with orchestrator
python make_it_heavy.py
# Input: "Use new feature across agents"
# Expected: All agents can use feature
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy . --ignore-missing-imports`
- [ ] Feature works in single agent mode
- [ ] Feature works in multi-agent mode
- [ ] Documentation updated
- [ ] Examples provided if applicable

---

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't modify core behavior without preserving compatibility