# PDB Agent Environment for LLMs

This package provides a Python debugger (pdb) agent environment that allows Large Language Models (LLMs) to debug Python code using pdb commands and execute code in a controlled environment.

## Overview

The main components of this package are:

1. `PdbAgentEnvironment`: Core environment that runs pdb on Python code
2. `PdbTools`: Tools interface for interacting with pdb
3. `LLMDebugAgent`: Agent that connects an LLM to the pdb environment
4. `llama3_integration.py`: Example integration with Llama3 (requires customization)

## Getting Started

### Installation

No special installation is required beyond the standard Python libraries. Simply ensure that you have Python installed with the required dependencies.

### Basic Usage

```python
from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler

# Initialize your LLM handler (example for Llama3)
llama3_handler = Llama3Handler(
    api_endpoint="https://your-llama3-api-endpoint.com",
    api_key="your-api-key"  # Optional
)

# Code to debug
buggy_code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Bug: Should be range(n - i - 1)
        for j in range(0, n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
"""

# Initialize the agent
debug_agent = LLMDebugAgent(
    llm_handler=llama3_handler,
    code=buggy_code,
    problem_description="The bubble sort function isn't working correctly."
)

# Run the debugging session
result = debug_agent.run()

# Print the fixed code
print(result["fixed_code"])
```

## Available Tools

The PDB Agent provides the following tools to the LLM:

1. `start_debugging`: Start a debugging session
2. `execute_pdb_command`: Execute a pdb command (e.g., n, s, p variable)
3. `execute_python_code`: Execute Python code in the debugger context
4. `stop_debugging`: Stop the debugging session
5. `get_pdb_help`: Get help information about available pdb commands
6. `examine_variable`: Examine the value of a variable
7. `set_breakpoint`: Set a breakpoint at the specified line number
8. `list_code`: List the code in the current file

## Customizing the LLM Integration

The `llama3_integration.py` file provides a placeholder for integrating with Llama3. You'll need to modify this file to work with your specific Llama3 API setup. The key function to implement is the `__call__` method, which should:

1. Take a system prompt, conversation history, and tools definition
2. Format these into a valid request for your LLM API
3. Send the request to the API and get the response
4. Parse the response and return it in a standardized format

## Examples

Check the `example_programs` directory for sample buggy programs and the `run_example.py` script for a demonstration of how to use the agent.

## Limitations

- The agent may not handle very complex debugging scenarios well
- The execution of arbitrary Python code poses security risks; use in controlled environments
- The performance depends heavily on the quality of the LLM being used

## Contributing

Feel free to submit issues or pull requests to improve this agent environment.