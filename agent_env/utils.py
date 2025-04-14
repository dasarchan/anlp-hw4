import os
import sys
import json
from typing import Dict, Optional, Any, List, Union

def read_code_from_file(file_path: str) -> str:
    """
    Read code from a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        String containing the code
    """
    with open(file_path, 'r') as f:
        return f.read()

def write_code_to_file(file_path: str, code: str) -> None:
    """
    Write code to a file.
    
    Args:
        file_path: Path to the file
        code: Code to write
    """
    with open(file_path, 'w') as f:
        f.write(code)

def save_debug_session(output_file: str, debug_session: Dict[str, Any]) -> None:
    """
    Save a debug session to a file.
    
    Args:
        output_file: Path to the output file
        debug_session: Debug session data to save
    """
    with open(output_file, 'w') as f:
        json.dump(debug_session, f, indent=2)

def load_debug_session(input_file: str) -> Dict[str, Any]:
    """
    Load a debug session from a file.
    
    Args:
        input_file: Path to the input file
        
    Returns:
        Dict containing the debug session data
    """
    with open(input_file, 'r') as f:
        return json.load(f)

def format_debug_conversation(conversation: List[Dict[str, Any]]) -> str:
    """
    Format a debug conversation for human-readable output.
    
    Args:
        conversation: List of conversation messages
        
    Returns:
        String containing the formatted conversation
    """
    output = []
    
    for message in conversation:
        role = message.get("role", "")
        
        if role == "user":
            output.append(f"\n--- USER ---\n{message.get('content', '')}")
        elif role == "assistant":
            output.append(f"\n--- ASSISTANT ---\n{message.get('content', '')}")
        elif role == "tool":
            tool_name = message.get("name", "")
            content = message.get("content", "")
            
            try:
                # Try to parse and pretty-print the content
                content_obj = json.loads(content)
                content = json.dumps(content_obj, indent=2)
            except:
                pass
                
            output.append(f"\n--- TOOL ({tool_name}) ---\n{content}")
    
    return "\n".join(output)

def debug_file_with_llm(
    file_path: str,
    llm_handler: Any,
    problem_description: Optional[str] = None,
    output_file: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_turns: int = 15
) -> Dict[str, Any]:
    """
    Debug a file using the LLM Debug Agent.
    
    Args:
        file_path: Path to the file to debug
        llm_handler: LLM handler to use
        problem_description: Optional problem description
        output_file: Optional path to save the debug session
        system_prompt: Optional system prompt
        max_turns: Maximum number of turns in the conversation
        
    Returns:
        Dict containing the debug session data
    """
    from .llm_agent import LLMDebugAgent
    
    # Read the code from the file
    code = read_code_from_file(file_path)
    
    # Initialize the debug agent
    debug_agent = LLMDebugAgent(
        llm_handler=llm_handler,
        code=code,
        problem_description=problem_description,
        system_prompt=system_prompt
    )
    
    # Run the debugging session
    result = debug_agent.run(max_turns=max_turns)
    
    # Save the debug session if output file is provided
    if output_file:
        save_debug_session(output_file, result)
    
    return result