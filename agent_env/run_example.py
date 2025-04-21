import os
import sys
import json
from typing import Dict, List, Any, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler, OpenAIHandler

# Example code with a bug
BUGGY_CODE = "\nclass Solution:\n    def restoreIpAddresses(self, s: str) -> List[str]:\n        res=[]\n        cur=[]\n        def backtrack(i):\n            if i==len(s) and len(cur)==4:\n                res.append(\".\".join(cur))\n                return\n            if len(cur)>4 or i>len(s):\n                return\n            if s[i]=='0':\n                cur.append(s[i])\n                backtrack(i+1)\n                cur.pop()\n                return\n            j=0\n            while j<4 and i+j<len(s)\n                if int(s[i:i+j+1])<256:\n                    cur.append(s[i:i+j+1])\n                    backtrack(i+j+1)\n                    cur.pop()\n                j+=1\n        backtrack(0)\n        return 'res\n"

PROBLEM_DESCRIPTION = "A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.\n\nFor example, \"0.1.2.201\" and \"192.168.1.1\" are valid IP addresses, but \"0.011.255.245\", \"192.168.1.312\" and \"192.168@1.1\" are invalid IP addresses.\n\nGiven a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s. You are not allowed to reorder or remove any digits in s. You may return the valid IP addresses in any order."


def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    openai_handler = OpenAIHandler(
        "gpt-4o-mini",
        api_key=openai_api_key,
    )
    
    # Initialize the LLM Debug Agent
    debug_agent = LLMDebugAgent(
        llm_handler=openai_handler,
        code=BUGGY_CODE,
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