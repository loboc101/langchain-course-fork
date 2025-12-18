# AI Coding Agent Instructions

## Project Overview
This is a LangChain-based agentic search tool that uses Large Language Models (LLMs) with tool access to perform web searches and return structured responses. The project demonstrates two agent implementation patterns: a simplified agent and a ReAct-style agent with prompt engineering.

## Architecture

### Core Components
- **`main.py`**: Simplified agent using `create_agent()` with GPT-5-nano, demonstrates structured output with `AgentResponse` schema
- **`main2.py`**: ReAct-style agent (Reason-Act) using `create_react_agent()` with GPT-4, more transparent reasoning with intermediate steps visible in verbose output
- **`schemas.py`**: Pydantic models defining structured outputs (`AgentResponse` with answer + sources list)
- **`prompt.py`**: ReAct prompt template with format instructions - essential for agent reasoning transparency

### Critical Data Flows
1. User query → LLM → Tool selection (TavilySearch)
2. Tool execution → Observation → LLM reasoning loop
3. Final reasoning → Structured output extraction via `with_structured_output()`

## Key Patterns

### Agent Configuration
- **LLM choice matters**: `main.py` uses nano model for speed, `main2.py` uses GPT-4 for reasoning quality. ReAct agents benefit from more capable models.
- **Tool integration**: Both agents use `TavilySearch()` tool. New tools should be added to the `tools` list and referenced in prompts.
- **Structured output**: Use `AgentResponse` schema (defined in `schemas.py`) as response format. Always include sources for traceability.

### ReAct Pattern (main2.py)
The ReAct agent is more complex but transparent:
- Custom prompt template in `prompt.py` controls agent behavior
- Chain pipeline: `agent_executor | extract_output | structured_llm` separates reasoning from output formatting
- `verbose=True` enables step-by-step debugging of agent thought process
- The `extract_output` Lambda extracts raw agent output before structural formatting

## Development Workflow

### Setup
```bash
uv init          # Initialize project
uv add <package> # Install dependencies
source .venv/bin/activate  # Activate virtual environment
```

### Dependencies
- **Core**: langchain, langchain-openai, langchain-tavily, langchainhub
- **Utils**: python-dotenv (environment variables), black, isort (code formatting)
- **Python**: >=3.12 required

### Running Agents
```bash
python main.py   # Simplified agent
python main2.py  # ReAct agent with reasoning
```

### Environment
- `.env` file required with API keys: `OPENAI_API_KEY`, `TAVILY_API_KEY`
- Use `load_dotenv()` from python-dotenv to load variables

## Project-Specific Conventions

### Prompting
- ReAct prompts use specific format: Question → Thought → Action → Action Input → Observation loop
- Format instructions are injected via prompt template partial (see `main2.py` line with `.partial(format_instructions="")`)
- The `{agent_scratchpad}` variable accumulates intermediate reasoning steps

### Schema Extension
To add new response fields:
1. Update `AgentResponse` in `schemas.py` with new `Field(description=...)`
2. Update ReAct prompt format instructions if the output structure changes
3. Test with `main2.py` to verify structured output validation

### Testing Patterns
- Both agents use simple input/query patterns in `main()` function
- For debugging: enable `verbose=True` in `AgentExecutor` to see full reasoning chain
- Test with varied query complexity: simple searches vs. multi-step reasoning requirements

## Cross-File Dependencies
- `main2.py` imports `REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS` from `prompt.py` - keep format consistent
- Both files import `AgentResponse` from `schemas.py` - schema changes affect both
- `langchainhub` pulls pre-built prompts (currently "hwchase17/react") - these can be overridden

## Common Modifications
- **Switch LLM**: Change `model="gpt-4"` parameter in ChatOpenAI initialization
- **Add tools**: Append to `tools` list and update prompt's `{tool_names}` section
- **Change output structure**: Modify `AgentResponse` schema and ReAct format instructions together
- **Adjust reasoning depth**: Modify ReAct prompt template in `prompt.py` to guide more/fewer reasoning steps
