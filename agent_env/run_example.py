import os
import sys
import json
from typing import Dict, List, Any, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler, OpenAIHandler

# Example code with a bug
BUBBLE_SORT_CODE = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Test the function
test_arr = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = bubble_sort(test_arr)
print(sorted_arr)
"""

PROBLEM_DESCRIPTION = """
The bubble_sort function is supposed to sort an array in ascending order using the bubble sort algorithm.
However, there seems to be a bug because the function is not correctly sorting the array.
Please debug the code and fix the issue.
"""

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    openai_handler = OpenAIHandler(
        "gpt-4o-mini",
        api_key=openai_api_key,
    )
    
    # Initialize the LLM Debug Agent
    debug_agent = LLMDebugAgent(
        llm_handler=openai_handler,
        code=BUBBLE_SORT_CODE,
        problem_description=PROBLEM_DESCRIPTION
    )
    
    # Run the debugging session
    result = debug_agent.run()
    
    # Print the results
    print("\n" + "="*50)
    print("DEBUGGING RESULTS")
    print("="*50)
    print("\nOriginal Code:")
    print(result["original_code"])
    
    print("\nFixed Code:")
    print(result["fixed_code"])
    
    print("\nNumber of turns:", result["turns"])
    
    # Save the full conversation history to a file
    with open("debug_conversation.json", "w") as f:
        json.dump(result["conversation"], f, indent=2)
    
    print("\nFull conversation history saved to debug_conversation.json")

if __name__ == "__main__":
    main()