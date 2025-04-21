import pexpect
import tempfile
import os
import sys
import time
from typing import Dict, Any, Optional

DEBUG = True

class PdbAgentEnvironment:
    def __init__(self, code: str, problem_description: Optional[str] = None):
        self.code = code
        self.problem_description = problem_description
        self.temp_file = None
        self.pdb_process = None
        self.is_active = False
        
    def start(self) -> Dict[str, Any]:
        # Create temporary file with the code
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False)
        self.temp_file.write(self.code)
        self.temp_file.flush()
        
        # Start pdb using pexpect
        cmd = f"{sys.executable} -m pdb {self.temp_file.name}"
        
        if DEBUG:
            print(f"Starting PDB with command: {cmd}")
            
        # Create pexpect child process
        try:
            self.pdb_process = pexpect.spawn(cmd, encoding='utf-8')
            
            # Uncomment to see all I/O in real-time for debugging:
            # self.pdb_process.logfile = sys.stdout
            
            # Wait for pdb prompt with sufficient timeout
            index = self.pdb_process.expect(['\\(Pdb\\)', pexpect.EOF, pexpect.TIMEOUT], timeout=5)
            
            if index == 0:  # Found the prompt
                initial_output = self.pdb_process.before + self.pdb_process.after
                self.is_active = True
                
                if DEBUG:
                    print(f"PDB started successfully: {initial_output}")
                    
                return {
                    "status": "started",
                    "output": initial_output,
                    "code": self.code,
                    "problem_description": self.problem_description
                }
            elif index == 1:  # EOF
                error_msg = f"PDB process ended unexpectedly: {self.pdb_process.before}"
                if DEBUG:
                    print(error_msg)
                return {"status": "error", "message": error_msg}
            else:  # TIMEOUT
                error_msg = f"Timeout waiting for PDB to start: {self.pdb_process.before}"
                if DEBUG:
                    print(error_msg)
                return {"status": "error", "message": error_msg}
                
        except Exception as e:
            error_msg = f"Error starting PDB: {str(e)}"
            if DEBUG:
                print(error_msg)
            return {"status": "error", "message": error_msg}
        
    def modify_code(self, code: str) -> None:
        """
        Modify the code in the temporary file.
        
        Args:
            code: The new code to write to the temporary file
        """
        self.code = code
    
    def execute_command(self, command: str, timeout: float = 10.0) -> Dict[str, Any]:
        if DEBUG:
            print(f"Executing command: {command}")
            
        if not self.is_active or self.pdb_process is None:
            return {"status": "error", "message": "Debugging session not active"}
            
        # Clear the buffer first to ensure we don't pick up previous output
        self.pdb_process.buffer = self.pdb_process.string_type()
        
        # Send command to pdb
        self.pdb_process.sendline(command)
        
        try:
            # First, expect to see the command echo'd back
            # This helps ensure we've moved past the previous prompt
            self.pdb_process.expect_exact(command, timeout=timeout)
            
            # Now wait for the next prompt after the command output
            index = self.pdb_process.expect(['\\(Pdb\\)', pexpect.EOF, pexpect.TIMEOUT], timeout=timeout)
            
            if index == 0:  # Found the prompt
                output = self.pdb_process.before
                if DEBUG:
                    print(f"Command output: {output}")

                if "post mortem" in output:
                    error_msg = "PDB process is in post mortem state."
                    if DEBUG:
                        print(error_msg)
                    self.is_active = False
                    self.pdb_process.close()
                return {
                    "status": "success",
                    "command": command,
                    "output": output
                }
            elif index == 1:  # EOF
                error_msg = f"PDB process ended during command execution: {self.pdb_process.before}"
                if DEBUG:
                    print(error_msg)
                self.is_active = False
                return {"status": "error", "message": error_msg}
            else:  # TIMEOUT
                error_msg = f"Timeout waiting for command completion: {self.pdb_process.before}"
                if DEBUG:
                    print(error_msg)
                return {"status": "timeout", "message": error_msg, "partial_output": self.pdb_process.before}
                
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            if DEBUG:
                print(error_msg)
            return {"status": "error", "message": error_msg}
    
    def execute_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in the debugger."""
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
        """Stop the debugging session."""
        if not self.is_active:
            return {"status": "already_stopped"}
            
        self.is_active = False
        
        # Try to exit gracefully first
        try:
            self.pdb_process.sendline("quit")
            self.pdb_process.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=2)
        except:
            pass
            
        # Force terminate if still running
        if self.pdb_process.isalive():
            self.pdb_process.close(force=True)
            
        # Clean up temp file
        if self.temp_file:
            try:
                os.unlink(self.temp_file.name)
            except:
                pass
                
        return {"status": "stopped"}