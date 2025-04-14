# PDB Agent Examples

This directory contains examples of how to use the PDB Agent environment with various LLMs.

## Files

- `llama3_real_integration.py`: An example of how to integrate with Llama3 (requires customization)

## Usage

To run an example:

```bash
cd /path/to/anlp-hw4
python -m agent_env.examples.llama3_real_integration
```

## Creating Your Own Integration

To create an integration with a different LLM:

1. Copy the `llama3_real_integration.py` file and rename it
2. Replace the API-specific code with your LLM's API
3. Run your integration following the same pattern as the examples

The key function to implement is the `__call__` method of your handler class, which should:
- Take a system prompt, conversation history, and tools definition
- Format these for your LLM API
- Send the request and get the response
- Parse the response into the standardized format expected by the agent