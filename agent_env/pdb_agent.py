import json
import os
import sys
import tempfile
import subprocess
from typing import Dict, List, Optional, Any, Tuple, Union
import threading

DEBUG=True

class PdbAgentEnvironment:
    """
    An environment that allows an LLM to interact with a Python debugger (pdb)
    to debug and solve Python exercises.
    """
    
    def __init__(self, code: str, problem_description: Optional[str] = None):
        """
        Initialize the PDB agent environment.
        
        Args:
            code: The Python code to debug
            problem_description: Optional description of the problem
        """
        self.code = code
        self.problem_description = problem_description
        self.temp_file = None
        self.pdb_process = None
        self.output_buffer = ""
        self.is_active = False
        
    def start(self) -> Dict[str, Any]:
        """
        Start the debugging session.
        
        Returns:
            Dict containing the initial state of the debugging session
        """
        # Create temporary file with the code
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
        self.temp_file.write(self.code)
        self.temp_file.flush()
        
        # Start the Python debugger on the temporary file
        cmd = [sys.executable, "-m", "pdb", self.temp_file.name]
        self.pdb_process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
        
        
        self.is_active = True
        
        # Read initial output
        initial_output = self._read_output()
        
        return {
            "status": "started",
            "output": initial_output,
            "code": self.code,
            "problem_description": self.problem_description
        }
    
    def modify_code(self, code: str) -> None:
        """
        Modify the code in the temporary file.
        
        Args:
            code: The new code to write to the temporary file
        """
        self.code = code
    
    def execute_command(self, command: str, timeout: float = 10.0) -> Dict[str, Any]:
        """
        Execute a pdb command.
        
        Args:
            command: The pdb command to execute
            timeout: Timeout in seconds for command execution (default: 10s)
            
        Returns:
            Dict containing the result of the command execution
        """
        if DEBUG:
            print(f"Command: {command}")
        if not self.is_active or self.pdb_process is None:
            return {"status": "error", "message": "Debugging session not active"}
        # Write command to pdb stdin
        self.pdb_process.stdin.write(command + "\n")
        self.pdb_process.stdin.flush()
        
        # Read output with timeout
        output = self._read_output(timeout=timeout)
        if DEBUG:
            print(f"Output: {output}")
        
        return {
            "status": "success",
            "command": command,
            "output": output
        }
    
    def execute_python(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code in the debugger.
        
        Args:
            code: Python code to execute
            
        Returns:
            Dict containing the result of the code execution
        """
        return self.execute_command("!{}".format(code))
    
    def _read_output(self, timeout: float = 0.5) -> str:
        """
        Read output from the pdb process.
        
        Args:
            timeout: Timeout in seconds for reading output
            
        Returns:
            String containing the output from pdb
        """
        import time
        import select
        
        output = ""
        start_time = time.time()
        
        while True:
            # Check if we have output to read using select with a short timeout
            ready_to_read, _, _ = select.select([self.pdb_process.stdout], [], [], 0.1)
            if self.pdb_process.stdout in ready_to_read:
                # Read one character at a time to avoid blocking
                char = self.pdb_process.stdout.read(1)
                if not char:
                    break
                output += char
            
            # Check if we've waited long enough or if the prompt is showing
            if (time.time() - start_time) > timeout or "(Pdb)" in output:
                break
        return output
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop the debugging session.
        
        Returns:
            Dict containing the final state of the debugging session
        """
        if self.is_active and self.pdb_process is not None:
            self.execute_command("quit")
            self.pdb_process.terminate()
            
            try:
                self.pdb_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.pdb_process.kill()
            
            self.is_active = False
            
            # Clean up temporary file
            if self.temp_file is not None:
                self.temp_file.close()
                os.unlink(self.temp_file.name)
                self.temp_file = None
        
        return {"status": "stopped"}