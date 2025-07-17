# Make It Heavy - Architecture & Planning

## Project Overview

Make It Heavy is a multi-agent AI system that emulates "Grok heavy" mode functionality, providing comprehensive, multi-perspective analysis through intelligent agent orchestration. The system has been enhanced with context engineering capabilities for improved agent performance.

## Architecture Decisions

### Core Architecture

1. **Agent System**
   - Single agent class (`OpenRouterAgent`) used for both modes
   - Context-aware agents that load project rules and examples
   - Agentic loop with max iterations for task completion
   - Tool discovery and execution system

2. **Multi-Agent Orchestration**
   - Parallel execution using ThreadPoolExecutor
   - Dynamic question generation for specialized perspectives
   - Response synthesis for comprehensive answers
   - Visual progress tracking for user feedback

3. **Context Engineering Integration**
   - Project context loaded from CLAUDE.md, PLANNING.md, TASK.md
   - PRP generation for complex feature implementation
   - Validation loops for self-correcting behavior
   - Example-based learning from codebase patterns

### Design Patterns

1. **Tool Pattern**
   - All tools inherit from `BaseTool`
   - Auto-discovery at import time
   - Consistent interface: name, description, parameters, execute
   - Error handling in each tool

2. **Context Pattern**
   - Centralized context loading through `ContextLoader`
   - Cached context for performance
   - Formatted context injection into prompts
   - Support for examples and PRPs

3. **Validation Pattern**
   - Multi-level validation: syntax, tests, integration
   - Self-correcting loops with error fixing
   - Automated validation through tools

## Technology Stack

- **LLM Provider**: OpenRouter API (configurable models)
- **Language**: Python 3.8+
- **Key Libraries**:
  - `openai`: OpenRouter client
  - `pydantic`: Data validation
  - `pyyaml`: Configuration
  - `ddgs`: DuckDuckGo search
  - `beautifulsoup4`: HTML parsing
  - `pytest`: Testing framework
  - `ruff`: Linting
  - `mypy`: Type checking

## Directory Structure

```
agent-creator/
├── Core Components
│   ├── agent.py              # Context-aware agent
│   ├── orchestrator.py       # Multi-agent coordination
│   └── config.yaml           # Configuration
│
├── Context System
│   ├── context/
│   │   ├── loader.py         # Project context loading
│   │   ├── models.py         # Data models
│   │   ├── prp_generator.py  # PRP generation
│   │   └── prp_executor.py   # PRP execution
│   │
│   ├── PRPs/                 # Product Requirements Prompts
│   │   └── templates/        # PRP templates
│   │
│   └── examples/             # Code examples for agents
│
├── Tool System
│   └── tools/
│       ├── base_tool.py      # Tool interface
│       ├── context_tool.py   # Context loading
│       ├── validation_tool.py # Code validation
│       └── [other tools]      # Search, file, calc, etc.
│
├── Documentation
│   ├── CLAUDE.md             # Project rules
│   ├── PLANNING.md           # This file
│   ├── TASK.md               # Task tracking
│   └── README.md             # User documentation
│
└── Testing
    └── tests/                # Unit tests
```

## Coding Standards

1. **Python Style**
   - PEP8 compliance enforced by ruff
   - Type hints for all functions
   - Google-style docstrings
   - Maximum line length: 120 characters

2. **Error Handling**
   - Specific exception types, not bare except
   - Graceful degradation for non-critical failures
   - Comprehensive error messages for debugging

3. **Testing Requirements**
   - Unit tests for all new features
   - Minimum 80% code coverage
   - Test happy path, edge cases, and errors
   - Integration tests for multi-agent features

4. **Documentation**
   - README.md for user-facing features
   - Docstrings for all public functions
   - Inline comments for complex logic
   - Examples for new patterns

## Performance Considerations

1. **Context Caching**
   - Project context loaded once and cached
   - Tool discovery happens at import time
   - Minimize file I/O operations

2. **API Rate Limiting**
   - Exponential backoff for OpenRouter
   - Respect model-specific rate limits
   - Parallel agents share rate limit budget

3. **Memory Management**
   - Stream responses for large outputs
   - Limit context size for low-window models
   - Clean up threads after orchestration

## Security Considerations

1. **API Keys**
   - Stored in config.yaml (gitignored)
   - Never logged or exposed in errors
   - Support for environment variables

2. **File Operations**
   - Validate all file paths
   - Restrict to project directory
   - Safe file reading/writing

3. **External APIs**
   - Validate all URLs
   - Timeout on all requests
   - Sanitize search results

## Future Enhancements

1. **RAG Integration**
   - Vector database for codebase search
   - Semantic code understanding
   - Dynamic example retrieval

2. **Advanced Orchestration**
   - Hierarchical agent structures
   - Dynamic agent spawning
   - Inter-agent communication

3. **Enhanced Validation**
   - AST-based code analysis
   - Automated performance testing
   - Security vulnerability scanning

## Maintenance Guidelines

1. **Adding New Tools**
   - Follow `BaseTool` pattern
   - Add comprehensive tests
   - Update documentation

2. **Modifying Core Components**
   - Preserve backward compatibility
   - Update all affected tests
   - Document breaking changes

3. **Updating Dependencies**
   - Test with all model providers
   - Verify tool compatibility
   - Update requirements.txt