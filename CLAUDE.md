### 🔄 Project Awareness & Context
- **Always check available tools** using the discover_tools system before implementing new functionality
- **Use the context loading system** to understand project rules and patterns
- **Follow existing patterns** in the codebase for consistency, especially the multi-agent orchestration patterns
- **Check PRPs directory** for implementation blueprints before starting complex features

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines**. Split into modules if approaching this limit.
- **Organize code into clearly separated modules** by feature:
  - `agent.py` - Core agent functionality
  - `orchestrator.py` - Multi-agent coordination
  - `tools/` - Individual tool implementations
  - `context/` - Context management system
- **Use clear, consistent imports** - prefer relative imports within packages
- **Follow the tool pattern** from `base_tool.py` when creating new tools

### 🧪 Testing & Reliability
- **Always create unit tests for new features** in the `/tests` directory
- **Mirror the test structure** from existing test files
- **Include test cases for**:
  - Happy path (expected use)
  - Edge cases (boundary conditions)
  - Error cases (failure scenarios)
- **Run validation** using the validation_tool before marking tasks complete

### ✅ Task Completion
- **Use the mark_task_complete tool** to signal when a task is finished
- **Include a summary** of what was accomplished
- **Update TASK.md** with completed work and any discovered tasks

### 📎 Style & Conventions
- **Use Python** as the primary language
- **Follow PEP8** style guidelines
- **Use type hints** for all function parameters and returns
- **Format with ruff** or black for consistency
- **Use pydantic** for data validation and models
- **Write Google-style docstrings** for all functions and classes:
  ```python
  def example(param: str) -> bool:
      """Brief description.
      
      Args:
          param: Description of parameter.
          
      Returns:
          Description of return value.
      """
  ```

### 📚 Documentation & Explainability
- **Update README.md** when adding major features or changing setup
- **Comment non-obvious code** with clear explanations
- **Add inline `# Reason:` comments** for complex logic
- **Document tool usage** in the tool's docstring

### 🔧 OpenRouter & API Integration
- **Handle rate limits** with exponential backoff for all API calls
- **Check model context windows** before sending large prompts
- **Use silent mode** for sub-agents to reduce output noise
- **Preserve API keys** in config.yaml, never hardcode

### 🏗️ Multi-Agent Patterns
- **Follow orchestrator patterns** from `orchestrator.py` for multi-agent tasks
- **Use ThreadPoolExecutor** for parallel agent execution
- **Implement proper error handling** for agent failures
- **Share context between agents** using the ProjectContext model

### 🧠 AI Behavior Rules
- **Never assume missing context** - use context_tool to load project information
- **Never hallucinate libraries** - only use packages in requirements.txt
- **Always validate file paths** before file operations
- **Check tool availability** before attempting to use tools
- **Follow PRP structure** when implementing features from PRPs

### 🛠️ Tool Development
- **Inherit from BaseTool** for all new tools
- **Implement all required properties**: name, description, parameters
- **Use proper error handling** in execute method
- **Return structured data** that agents can parse
- **Add new tools to auto-discovery** by placing in tools/ directory