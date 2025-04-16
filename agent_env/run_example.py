import os
import sys
import json
from typing import Dict, List, Any, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler, OpenAIHandler

# Example code with a bug
BUBBLE_SORT_CODE = "\nclass Solution:\n    def makeSmallestPalindrome(self, s: str) -> str\n        before = 0\n        after = len(s)-1\n        l = [i for i in s]\n        while before <= len(s)\n            l[before] = self.min(l[before], l[after])\n            l[after] = l[before]\n            before+=1\n            after-=1\n        return \"\".join(l)\n"

PROBLEM_DESCRIPTION = "You are given a string s consisting of lowercase English letters, and you are allowed to perform operations on it. In one operation, you can replace a character in s with another lowercase English letter.\nYour task is to make s a palindrome with the minimum number of operations possible. If there are multiple palindromes that can be made using the minimum number of operations, make the lexicographically smallest one.\nA string a is lexicographically smaller than a string b (of the same length) if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b.\nReturn the resulting palindrome string."


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