#!/usr/bin/env python3
import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional

from .utils import debug_file_with_llm, format_debug_conversation
from .llama3_integration import Llama3Handler

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Debug Python files using an LLM with pdb"
    )
    
    parser.add_argument(
        "file_path",
        type=str,
        help="Path to the Python file to debug"
    )
    
    parser.add_argument(
        "--api-endpoint",
        type=str,
        default=os.environ.get("LLAMA3_API_ENDPOINT", ""),
        help="Llama3 API endpoint (can also set LLAMA3_API_ENDPOINT env var)"
    )
    
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.environ.get("LLAMA3_API_KEY", ""),
        help="Llama3 API key (can also set LLAMA3_API_KEY env var)"
    )
    
    parser.add_argument(
        "--problem",
        type=str,
        help="Description of the problem to solve"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save the debug session JSON"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print the full conversation"
    )
    
    parser.add_argument(
        "--system-prompt",
        type=str,
        help="Path to a file containing a custom system prompt"
    )
    
    parser.add_argument(
        "--max-turns",
        type=int,
        default=15,
        help="Maximum number of turns in the conversation"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # Check if the file exists
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        sys.exit(1)
    
    # Check if the API endpoint is provided
    if not args.api_endpoint:
        print("Error: Llama3 API endpoint is required. Provide it with --api-endpoint or set LLAMA3_API_ENDPOINT env var.")
        sys.exit(1)
    
    # Load custom system prompt if provided
    system_prompt = None
    if args.system_prompt:
        if os.path.exists(args.system_prompt):
            with open(args.system_prompt, 'r') as f:
                system_prompt = f.read()
        else:
            print(f"Warning: System prompt file not found: {args.system_prompt}")
    
    # Initialize the Llama3 handler
    llama3_handler = Llama3Handler(args.api_endpoint, args.api_key)
    
    print(f"Debugging file: {args.file_path}")
    if args.problem:
        print(f"Problem description: {args.problem}")
    
    # Debug the file
    result = debug_file_with_llm(
        file_path=args.file_path,
        llm_handler=llama3_handler,
        problem_description=args.problem,
        output_file=args.output,
        system_prompt=system_prompt,
        max_turns=args.max_turns
    )
    
    # Print results
    print("\n" + "="*50)
    print("DEBUGGING RESULTS")
    print("="*50)
    
    if args.verbose:
        # Print the full conversation
        print("\nCONVERSATION:")
        print(format_debug_conversation(result["conversation"]))
    
    print("\nFIXED CODE:")
    print(result["fixed_code"])
    
    if args.output:
        print(f"\nDebug session saved to: {args.output}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())