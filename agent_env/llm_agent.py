import json
import os
import sys
from typing import Dict, List, Any, Optional, Callable, Union

from .pdb_agent import PdbAgentEnvironment
from .tools.pdb_tools import PdbTools

class LLMDebugAgent:
    """
    An agent that uses an LLM to debug Python code with pdb.
    """
    
    def __init__(
        self, 
        llm_handler: Callable[[str, List[Dict[str, Any]]], Dict[str, Any]],
        code: str, 
        problem_description: Optional[str] = None,
        system_prompt: Optional[str] = None
    ):
        """
        Initialize the LLM Debug Agent.
        
        Args:
            llm_handler: A function that takes a prompt and available tools, and returns the LLM's response
            code: The Python code to debug
            problem_description: Optional description of the problem
            system_prompt: Optional system prompt for the LLM
        """
        self.code = code
        self.problem_description = problem_description
        self.llm_handler = llm_handler
        
        # Set up the PDB environment
        self.pdb_env = PdbAgentEnvironment(code, problem_description)
        self.pdb_tools = PdbTools(self.pdb_env)
        
        # Default system prompt if none is provided
        if system_prompt is None:
            self.system_prompt = """
You are a Python debugging assistant. Your task is to help fix bugs in the code using the Python debugger (pdb).
You have access to a set of tools that allow you to interact with pdb.

The main pdb commands you can use include:
- h (help): Print the list of available commands
- n (next): Continue execution until the next line
- s (step): Execute the current line, stop at the first possible occasion
- c (continue): Continue execution until next breakpoint
- p expression: Print the value of the expression
- pp expression: Pretty-print the value of the expression
- l (list): List source code around the current line
- b (break) lineno: Set a breakpoint at the specified line
- r (return): Continue execution until the current function returns
- q (quit): Quit from the debugger
- ! statement: Execute the Python statement in the current context

You can also start and stop debugging, as well as modify the underlying code.

If debugging stops, you can restart it after modifying code. You need to restart for modify_code to take effect.

Approach:
1. First, understand the problem and the code
2. Use the debugger to step through the code and examine variables
3. Identify the bug(s) and propose a fix
4. Test the fix to ensure it resolves the issue

Remember to explain your reasoning as you debug, so the user understands the process.

If you believe you have the answer, write 'FIXED_CODE' and then a python block with your solution.
This is very important! Without writing FIXED_CODE your solution will not be considered.
"""
        else:
            self.system_prompt = system_prompt
        
        # Conversation history
        self.conversation_history = []
        
    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get the list of available tools in a format suitable for function calling.
        
        Returns:
            List of tool definitions
        """
        tools_dict = self.pdb_tools.get_available_tools()
        
        tools = []
        for tool_name, tool_info in tools_dict.items():
            params = {}
            required = []
            
            for param_name, param_desc in tool_info.get("parameters", {}).items():
                param_type = "string"
                if param_name == "line_number":
                    param_type = "integer"
                
                param_def = {
                    "type": param_type,
                    "description": param_desc
                }
                
                # Mark all parameters as required except condition and start/end_line
                if param_name not in ["condition", "start_line", "end_line"]:
                    required.append(param_name)
                
                params[param_name] = param_def
            
            tool = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_info["description"],
                    "parameters": {
                        "type": "object",
                        "properties": params,
                        "required": required
                    }
                }
            }
            
            tools.append(tool)
            
        return tools
    
    def _execute_tool(self, tool_name: str, tool_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool based on name and parameters.
        
        Args:
            tool_name: The name of the tool to execute
            tool_params: Parameters for the tool
            
        Returns:
            Dict containing the result of the tool execution
        """
        if tool_name == "start_debugging":
            return self.pdb_tools.start_debugging()
        if tool_name == "modify_code":
            self.pdb_tools.modify_code(tool_params["code"])
        elif tool_name == "execute_pdb_command":
            return self.pdb_tools.execute_pdb_command(tool_params["command"])
        elif tool_name == "execute_python_code":
            return self.pdb_tools.execute_python_code(tool_params["code"])
        elif tool_name == "stop_debugging":
            return self.pdb_tools.stop_debugging()
        elif tool_name == "get_pdb_help":
            return self.pdb_tools.get_pdb_help()
        elif tool_name == "examine_variable":
            return self.pdb_tools.examine_variable(tool_params["variable_name"])
        elif tool_name == "set_breakpoint":
            condition = tool_params.get("condition")
            return self.pdb_tools.set_breakpoint(tool_params["line_number"], condition)
        elif tool_name == "list_code":
            start_line = tool_params.get("start_line")
            end_line = tool_params.get("end_line")
            return self.pdb_tools.list_code(start_line, end_line)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def run(self, max_turns: int = 15) -> Dict[str, Any]:
        """
        Run the debugging session with the LLM.
        
        Args:
            max_turns: Maximum number of turns in the conversation
            
        Returns:
            Dict containing the result of the debugging session
        """
        # Start with initial prompt
        prompt = f"""
I need help debugging the following Python code:

```python
{self.code}
```
        """
        
        if self.problem_description:
            prompt += f"""
Problem description:
{self.problem_description}

Please help me debug this code to solve the problem.
"""
        else:
            prompt += """
Please help me identify and fix any bugs in this code.
"""
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Run the conversation
        turn_count = 0
        while turn_count < max_turns:
            turn_count += 1
            
            # Get LLM's response
            tools = self._get_available_tools()
            llm_response = self.llm_handler(
                self.system_prompt,
                self.conversation_history,
                tools
            )
            
            # Add LLM's response to conversation history
            self.conversation_history.append(llm_response)
            
            # Check if the response contains a tool call
            tool_calls = llm_response.get("tool_calls", [])
            if tool_calls:
                for tool_call in tool_calls:
                    function = tool_call.get("function", {})
                    tool_name = function.get("name")
                    
                    # Parse tool parameters from JSON string
                    try:
                        tool_params = json.loads(function.get("arguments", "{}"))
                    except:
                        tool_params = {}
                    
                    # Execute the tool
                    tool_result = self._execute_tool(tool_name, tool_params)
                    
                    # Add tool result to conversation history
                    self.conversation_history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "name": tool_name,
                        "content": json.dumps(tool_result)
                    })
            
            # Check for any "finished" indication in the response
            content = llm_response.get("content", "")
            if "DEBUGGING_COMPLETE" in content or "FIXED_CODE" in content or "FINAL_SOLUTION" in content:
                break
        
        # Extract the fixed code from the conversation
        fixed_code = self._extract_fixed_code()
        
        return {
            "original_code": self.code,
            "fixed_code": fixed_code,
            "conversation": self.conversation_history,
            "turns": turn_count
        }
    
    def _extract_fixed_code(self) -> str:
        """
        Extract the fixed code from the conversation history.
        
        Returns:
            String containing the fixed code
        """
        # Look for the fixed code in the assistant's last few messages
        for message in reversed(self.conversation_history):
            if message.get("role") == "assistant":
                content = message.get("content", "")
                
                # Check if FIXED_CODE is in the content
                if "FIXED_CODE" in content:
                    # Look for the first Python code block after FIXED_CODE
                    import re
                    code_blocks = re.findall(r"```python\n(.*?)\n```", content, re.DOTALL)
                    if code_blocks:
                        return code_blocks[0]
                        
                # If we're here, either FIXED_CODE wasn't found or there was no code block
        
        # If no fixed code found, return original code
        return self.code