name: "Agent Creator Context Engineering Integration PRP"
description: |

## Purpose
Enhance the make-it-heavy agent system with comprehensive context engineering capabilities, allowing agents to leverage project-specific context, examples, and validation loops for higher quality implementations.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md

---

## Goal
Transform the make-it-heavy agent system into a context-aware multi-agent platform that can:
- Load and use project-specific context from CLAUDE.md files
- Generate and execute PRPs (Product Requirements Prompts) for complex tasks
- Provide agents with code examples and patterns from the codebase
- Implement validation loops for self-correcting behavior
- Support context-aware tool creation and discovery

## Why
- **Business value**: Dramatically improves agent success rates by providing comprehensive context
- **Integration**: Seamlessly integrates with existing multi-agent orchestration
- **Problems solved**: Reduces agent failures due to missing context, ensures consistency with project patterns

## What
Enhanced agent system with:
- Context loading from CLAUDE.md and project files
- PRP generation and execution capabilities
- Example-based learning for agents
- Validation and self-correction loops
- Context-aware tool system

### Success Criteria
- [ ] Agents can load and use CLAUDE.md context
- [ ] PRP generation creates comprehensive implementation blueprints
- [ ] Agents follow project patterns from examples
- [ ] Validation loops ensure code quality
- [ ] All existing functionality preserved
- [ ] Tests pass with 100% coverage for new features

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- file: /home/vedant112/agent-creator/agent.py
  why: Core agent implementation to enhance with context awareness
  
- file: /home/vedant112/agent-creator/orchestrator.py
  why: Orchestrator patterns for multi-agent context sharing
  
- file: /home/vedant112/agent-creator/tools/base_tool.py
  why: Tool interface to extend with context capabilities
  
- file: /home/vedant112/agent-creator/config.yaml
  why: Configuration patterns and agent prompts
  
- file: /home/vedant112/agent-creator/context-template/CLAUDE.md
  why: Example of project context rules
  
- file: /home/vedant112/agent-creator/context-template/PRPs/templates/prp_base.md
  why: PRP template structure to implement

- docfile: context-template/README.md
  why: Full context engineering methodology and workflow
```

### Current Codebase Structure
```bash
agent-creator/
├── agent.py                 # Core agent implementation
├── orchestrator.py         # Multi-agent orchestration
├── config.yaml             # Configuration and prompts
├── main.py                 # Single agent CLI
├── make_it_heavy.py        # Multi-agent CLI
├── requirements.txt        # Dependencies
└── tools/                  # Tool system
    ├── __init__.py         # Auto-discovery
    ├── base_tool.py        # Tool interface
    ├── search_tool.py      # Web search
    ├── calculator_tool.py  # Math
    ├── read_file_tool.py   # File reading
    ├── write_file_tool.py  # File writing
    └── task_done_tool.py   # Task completion
```

### Desired Codebase Structure
```bash
agent-creator/
├── agent.py                 # Enhanced with context loading
├── orchestrator.py         # Enhanced with PRP execution
├── config.yaml             # Updated prompts for context awareness
├── main.py                 # Single agent CLI
├── make_it_heavy.py        # Multi-agent CLI
├── requirements.txt        # Dependencies
├── CLAUDE.md               # Project-specific rules
├── PLANNING.md             # Architecture documentation
├── TASK.md                 # Task tracking
├── context/
│   ├── __init__.py         # Context management package
│   ├── loader.py           # Load CLAUDE.md and project context
│   ├── prp_generator.py    # Generate PRPs from requirements
│   └── prp_executor.py     # Execute PRPs with validation
├── tools/
│   ├── __init__.py         # Enhanced discovery with context
│   ├── base_tool.py        # Enhanced with context awareness
│   ├── context_tool.py     # New: Load project context
│   ├── prp_tool.py         # New: Generate/execute PRPs
│   ├── validation_tool.py  # New: Run tests and linting
│   └── [existing tools]
├── examples/               # Code examples for agents
│   ├── README.md           # Explains examples
│   ├── agent_patterns.py   # Agent creation patterns
│   ├── tool_patterns.py    # Tool implementation patterns
│   └── test_patterns.py    # Testing patterns
├── tests/
│   ├── __init__.py
│   ├── test_agent.py       # Agent tests
│   ├── test_context.py     # Context system tests
│   ├── test_tools.py       # Tool tests
│   └── test_orchestrator.py # Orchestrator tests
└── PRPs/                   # Generated PRPs
    └── templates/
        └── prp_base.md     # Base PRP template
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: OpenRouter API has rate limits - implement exponential backoff
# Example: Some models have low context windows - check before loading large contexts
# Example: YAML safe_load doesn't preserve comments - use ruamel.yaml if needed
# Example: Tool discovery happens at import time - new tools require restart
# Example: Async operations in tools need proper error handling
```

## Implementation Blueprint

### Data Models and Structure

```python
# context/models.py - Core data models for context system
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class ContextType(str, Enum):
    CLAUDE_MD = "claude_md"
    PLANNING = "planning"
    TASK = "task"
    EXAMPLE = "example"
    PRP = "prp"

class ProjectContext(BaseModel):
    """Complete project context for agents"""
    claude_rules: str = Field(description="Content of CLAUDE.md")
    planning: Optional[str] = Field(description="Content of PLANNING.md")
    tasks: Optional[str] = Field(description="Content of TASK.md")
    examples: Dict[str, str] = Field(default_factory=dict, description="Example code files")
    prps: Dict[str, str] = Field(default_factory=dict, description="Available PRPs")
    
class PRPRequest(BaseModel):
    """Request to generate a PRP"""
    feature_description: str
    examples: List[str] = Field(default_factory=list)
    documentation_urls: List[str] = Field(default_factory=list)
    considerations: Optional[str] = None

class ValidationResult(BaseModel):
    """Result of code validation"""
    success: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    fixed_code: Optional[str] = None
```

### Implementation Tasks

```yaml
Task 1: Create Context Management System
CREATE context/__init__.py:
  - Import all context components
  - Export public API

CREATE context/loader.py:
  - PATTERN: Use pathlib for cross-platform paths
  - Load CLAUDE.md, PLANNING.md, TASK.md
  - Discover and load examples directory
  - Cache loaded context for performance
  - Handle missing files gracefully

CREATE context/models.py:
  - Copy data models from blueprint above
  - Add validation for required fields
  - Include serialization methods

Task 2: Enhance Agent with Context Awareness
MODIFY agent.py:
  - FIND: "__init__" method of OpenRouterAgent
  - ADD: context_loader parameter and initialization
  - INJECT: Context into system prompt
  - PRESERVE: All existing functionality

Task 3: Create Context-Aware Tools
CREATE tools/context_tool.py:
  - MIRROR: Pattern from read_file_tool.py
  - Implement load_project_context function
  - Return structured ProjectContext

CREATE tools/prp_tool.py:
  - MIRROR: Pattern from base_tool.py
  - Implement generate_prp function
  - Use context to create comprehensive PRPs

CREATE tools/validation_tool.py:
  - Implement run_tests, run_linting functions
  - Support pytest, ruff, mypy
  - Return structured validation results

Task 4: Create PRP Generator
CREATE context/prp_generator.py:
  - PATTERN: Use OpenRouterAgent for AI generation
  - Load PRP template from PRPs/templates/
  - Research codebase for patterns
  - Generate comprehensive PRPs with validation

Task 5: Create PRP Executor  
CREATE context/prp_executor.py:
  - Parse PRP structure
  - Create task list with TodoWrite pattern
  - Execute tasks with validation loops
  - Handle errors and iterate

Task 6: Update Configuration
MODIFY config.yaml:
  - UPDATE: system_prompt to include context awareness
  - ADD: Context-specific prompts for PRP generation
  - PRESERVE: All existing configuration

Task 7: Create Project Documentation
CREATE CLAUDE.md:
  - Copy template from context-template
  - Customize for make-it-heavy project
  - Include Python best practices

CREATE PLANNING.md:
  - Document architecture decisions
  - Explain context integration
  - Define coding standards

CREATE TASK.md:
  - Initialize with current tasks
  - Include discovered work section

Task 8: Create Examples
CREATE examples/README.md:
  - Explain each example's purpose
  - Include usage instructions

CREATE examples/agent_patterns.py:
  - Show agent creation patterns
  - Include context loading examples

CREATE examples/tool_patterns.py:
  - Show tool implementation patterns
  - Include error handling

Task 9: Create Comprehensive Tests
CREATE tests/test_context.py:
  - Test context loading
  - Test PRP generation
  - Test validation loops

CREATE tests/test_agent.py:
  - Test context-aware agents
  - Test tool integration
  - Test error scenarios

Task 10: Update Documentation
MODIFY README.md:
  - ADD: Context engineering section
  - ADD: PRP workflow documentation
  - UPDATE: Usage examples with context
```

### Per-Task Pseudocode

```python
# Task 1: Context Loader Implementation
# context/loader.py
class ContextLoader:
    def __init__(self, project_root: Path = None):
        self.root = project_root or Path.cwd()
        self._cache = {}
    
    def load_project_context(self) -> ProjectContext:
        # PATTERN: Check cache first for performance
        if "project_context" in self._cache:
            return self._cache["project_context"]
        
        # PATTERN: Load each file with graceful fallbacks
        claude_rules = self._load_file("CLAUDE.md", required=True)
        planning = self._load_file("PLANNING.md", required=False)
        tasks = self._load_file("TASK.md", required=False)
        
        # PATTERN: Discover examples using glob
        examples = {}
        examples_dir = self.root / "examples"
        if examples_dir.exists():
            for py_file in examples_dir.glob("*.py"):
                examples[py_file.name] = py_file.read_text()
        
        # CRITICAL: Validate and cache
        context = ProjectContext(
            claude_rules=claude_rules,
            planning=planning,
            tasks=tasks,
            examples=examples
        )
        self._cache["project_context"] = context
        return context

# Task 2: Enhanced Agent
# Modification to agent.py
class OpenRouterAgent:
    def __init__(self, config_path="config.yaml", silent=False, context_loader=None):
        # ... existing init code ...
        
        # NEW: Context integration
        self.context_loader = context_loader or ContextLoader()
        self.project_context = self.context_loader.load_project_context()
        
        # PATTERN: Inject context into system prompt
        enhanced_prompt = self._enhance_prompt_with_context(
            self.config['system_prompt'],
            self.project_context
        )
        
    def _enhance_prompt_with_context(self, base_prompt, context):
        # CRITICAL: Format context for LLM consumption
        context_section = f"""
## Project Context

### Rules (from CLAUDE.md):
{context.claude_rules}

### Available Examples:
{chr(10).join(f"- {name}" for name in context.examples.keys())}
"""
        return base_prompt + context_section

# Task 4: PRP Generator
# context/prp_generator.py
class PRPGenerator:
    def __init__(self, agent: OpenRouterAgent):
        self.agent = agent
        self.template = self._load_template()
    
    async def generate_prp(self, request: PRPRequest) -> str:
        # PATTERN: Research codebase first
        research_results = await self._research_codebase(request)
        
        # PATTERN: Load relevant documentation
        docs = await self._fetch_documentation(request.documentation_urls)
        
        # CRITICAL: Use template with all context
        prompt = f"""
Generate a comprehensive PRP using this template:
{self.template}

Feature Request:
{request.feature_description}

Research Results:
{research_results}

Documentation:
{docs}
"""
        # PATTERN: Use agent to generate PRP
        prp_content = self.agent.run(prompt)
        
        # VALIDATE: Ensure all sections present
        self._validate_prp_structure(prp_content)
        
        return prp_content
```

### Integration Points
```yaml
CONFIG:
  - add to: config.yaml
  - section: "context_engineering"
  - pattern: |
      context_engineering:
        enable_context_loading: true
        prp_template_path: "PRPs/templates/prp_base.md"
        validation_commands:
          lint: "ruff check {file} --fix"
          type_check: "mypy {file}"
          test: "pytest {test_file} -v"

TOOLS:
  - modify: tools/__init__.py
  - pattern: "Auto-discover and inject context into tools"
  
PROMPTS:
  - modify: config.yaml system_prompt
  - add: "Always check project context before implementing"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check . --fix              # Auto-fix style issues
mypy agent.py context/          # Type checking

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# tests/test_context.py
def test_context_loader_loads_claude_md():
    """Context loader successfully loads CLAUDE.md"""
    loader = ContextLoader(test_project_root)
    context = loader.load_project_context()
    assert context.claude_rules is not None
    assert "Project Awareness" in context.claude_rules

def test_prp_generator_creates_valid_prp():
    """PRP generator creates properly structured PRPs"""
    generator = PRPGenerator(mock_agent)
    request = PRPRequest(feature_description="Add caching")
    prp = generator.generate_prp(request)
    assert "## Goal" in prp
    assert "## Validation Loop" in prp

def test_agent_uses_context_in_prompt():
    """Agent includes context in system prompt"""
    agent = OpenRouterAgent(context_loader=mock_loader)
    messages = agent._build_messages("test")
    system_prompt = messages[0]["content"]
    assert "CLAUDE.md" in system_prompt
```

```bash
# Run and iterate until passing:
pytest tests/test_context.py -v
pytest tests/ -v  # All tests
```

### Level 3: Integration Test
```bash
# Test context-aware agent
python main.py
# Input: "Show me the project context"
# Expected: Agent describes CLAUDE.md rules

# Test PRP generation
python main.py
# Input: "Generate a PRP for adding Redis caching"
# Expected: Complete PRP saved to PRPs/

# Test heavy mode with context
python make_it_heavy.py
# Input: "Implement the Redis caching PRP"
# Expected: All agents use context, follow patterns
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy . --ignore-missing-imports`
- [ ] Context loads successfully in both CLI modes
- [ ] Agents follow CLAUDE.md rules
- [ ] PRPs generate with all required sections
- [ ] Examples are used by agents
- [ ] Validation loops work correctly
- [ ] Documentation updated in README.md

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode paths - use Path objects
- ❌ Don't ignore context loading errors - handle gracefully
- ❌ Don't skip validation - it ensures quality
- ❌ Don't modify existing behavior - enhance it
- ❌ Don't create circular dependencies between modules
- ❌ Don't load context on every call - cache appropriately