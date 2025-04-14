from typing import Dict, Any, List, Optional
import json

class PdbTools:
    """
    A collection of tools that allow an LLM to interact with the PDB debugger.
    These can be exposed as function calling capabilities to the LLM.
    """
    
    def __init__(self, pdb_env):
        """
        Initialize the PDB tools.
        
        Args:
            pdb_env: The PDB agent environment
        """
        self.pdb_env = pdb_env
        
    def start_debugging(self) -> Dict[str, Any]:
        """
        Start a debugging session.
        
        Returns:
            Dict containing the initial state of the debugging session
        """
        return self.pdb_env.start()
    
    def execute_pdb_command(self, command: str) -> Dict[str, Any]:
        """
        Execute a pdb command.
        
        Args:
            command: The pdb command to execute (e.g., "n", "s", "p variable_name")
            
        Returns:
            Dict containing the result of the command execution
        """
        return self.pdb_env.execute_command(command)
    
    def execute_python_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in the debugger context.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict containing the result of the code execution
        """
        return self.pdb_env.execute_python(code)
    
    def stop_debugging(self) -> Dict[str, Any]:
        """
        Stop the debugging session.
        
        Returns:
            Dict containing the final state of the debugging session
        """
        return self.pdb_env.stop()
    
    def get_pdb_help(self) -> Dict[str, Any]:
        """
        Get help information about available pdb commands.
        
        Returns:
            Dict containing help information about pdb commands
        """
        return self.pdb_env.execute_command("help")
    
    def examine_variable(self, variable_name: str) -> Dict[str, Any]:
        """
        Examine the value of a variable.
        
        Args:
            variable_name: The name of the variable to examine
            
        Returns:
            Dict containing the value of the variable
        """
        return self.pdb_env.execute_command(f"p {variable_name}")
    
    def set_breakpoint(self, line_number: int, condition: Optional[str] = None) -> Dict[str, Any]:
        """
        Set a breakpoint at the specified line number with an optional condition.
        
        Args:
            line_number: The line number for the breakpoint
            condition: Optional condition for the breakpoint
            
        Returns:
            Dict containing the result of setting the breakpoint
        """
        command = f"break {line_number}"
        if condition:
            command += f", {condition}"
        return self.pdb_env.execute_command(command)
    
    def list_code(self, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
        """
        List the code in the current file.
        
        Args:
            start_line: Optional starting line number
            end_line: Optional ending line number
            
        Returns:
            Dict containing the listed code
        """
        command = "list"
        if start_line is not None and end_line is not None:
            command = f"list {start_line}, {end_line}"
        elif start_line is not None:
            command = f"list {start_line}"
        return self.pdb_env.execute_command(command)
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a description of all available tools.
        
        Returns:
            Dict containing descriptions of all available tools
        """
        tools = {
            "start_debugging": {
                "description": "Start a debugging session",
                "parameters": {}
            },
            "execute_pdb_command": {
                "description": "Execute a pdb command",
                "parameters": {
                    "command": "The pdb command to execute (e.g., 'n', 's', 'p variable_name')"
                }
            },
            "execute_python_code": {
                "description": "Execute Python code in the debugger context",
                "parameters": {
                    "code": "Python code to execute"
                }
            },
            "stop_debugging": {
                "description": "Stop the debugging session",
                "parameters": {}
            },
            "get_pdb_help": {
                "description": "Get help information about available pdb commands",
                "parameters": {}
            },
            "examine_variable": {
                "description": "Examine the value of a variable",
                "parameters": {
                    "variable_name": "The name of the variable to examine"
                }
            },
            "set_breakpoint": {
                "description": "Set a breakpoint at the specified line number with an optional condition",
                "parameters": {
                    "line_number": "The line number for the breakpoint",
                    "condition": "Optional condition for the breakpoint"
                }
            },
            "list_code": {
                "description": "List the code in the current file",
                "parameters": {
                    "start_line": "Optional starting line number",
                    "end_line": "Optional ending line number"
                }
            }
        }
        return tools