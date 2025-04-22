import os
import sys
import json
from typing import Dict, List, Any, Optional
from tqdm import tqdm

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets import load_dataset
from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler, OpenAIHandler

# Example code with a bug
BUGGY_CODE = "\nclass Solution:\n    def restoreIpAddresses(self, s: str) -> List[str]:\n        res=[]\n        cur=[]\n        def backtrack(i):\n            if i==len(s) and len(cur)==4:\n                res.append(\".\".join(cur))\n                return\n            if len(cur)>4 or i>len(s):\n                return\n            if s[i]=='0':\n                cur.append(s[i])\n                backtrack(i+1)\n                cur.pop()\n                return\n            j=0\n            while j<4 and i+j<len(s)\n                if int(s[i:i+j+1])<256:\n                    cur.append(s[i:i+j+1])\n                    backtrack(i+j+1)\n                    cur.pop()\n                j+=1\n        backtrack(0)\n        return 'res\n"

PROBLEM_DESCRIPTION = "A valid IP address consists of exactly four integers separated by single dots. Each integer is between 0 and 255 (inclusive) and cannot have leading zeros.\n\nFor example, \"0.1.2.201\" and \"192.168.1.1\" are valid IP addresses, but \"0.011.255.245\", \"192.168.1.312\" and \"192.168@1.1\" are invalid IP addresses.\n\nGiven a string s containing only digits, return all possible valid IP addresses that can be formed by inserting dots into s. You are not allowed to reorder or remove any digits in s. You may return the valid IP addresses in any order."



def execute_debug_agent(code, problem_description, openai_handler):
    # Initialize the LLM Debug Agent
    debug_agent = LLMDebugAgent(
        llm_handler=openai_handler,
        code=code,
        problem_description=problem_description,
    )

    # Run the debugging session
    result = debug_agent.run()

    # Print the results
<<<<<<< HEAD
    # print("\n" + "=" * 50)
    # print("DEBUGGING RESULTS")
    # print("=" * 50)
    # print("\nOriginal Code:")
    # print(result["original_code"])
=======
    print("\n" + "=" * 50)
    print("DEBUGGING RESULTS")
    print("=" * 50)
    print("\nOriginal Code:")
    print(result["original_code"])
>>>>>>> 0a3fd3b (some init result)

    print("\nFixed Code:")
    print(result["fixed_code"])

    print("\nNumber of turns:", result["turns"])

    # Save the full conversation history to a file
<<<<<<< HEAD
    # with open("debug_conversation.json", "w") as f:
    #     json.dump(result["conversation"], f, indent=2)

    # print("\nFull conversation history saved to debug_conversation.json")
=======
    with open("debug_conversation.json", "w") as f:
        json.dump(result["conversation"], f, indent=2)

    print("\nFull conversation history saved to debug_conversation.json")
>>>>>>> 0a3fd3b (some init result)
    return result["fixed_code"], result["turns"], result["conversation"]

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")

    openai_handler = OpenAIHandler(
        "gpt-3.5-turbo",
        api_key=openai_api_key,
    )
    data = load_dataset("Rtian/DebugBench")
    python3_instances = [
        example for example in data["test"] if example["language"] == "python3"
    ]
    
    results_file = "debug_results.json"    
    # Load existing results if file exists
    results = {}
    if os.path.exists(results_file):
        try:
            with open(results_file, "r") as f:
                results = json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {results_file}, starting with empty results")
        
    for i in tqdm(range(len(python3_instances)), desc="Processing examples"):
        id = (python3_instances[i]["slug"], python3_instances[i]["category"])
        code = python3_instances[i]["buggy_code"]
        problem_description = python3_instances[i]["question"]
        
        result_key = f"{id[0]}_{id[1]}"
        
        # Skip if this example has already been processed
        if result_key in results:
            print(f"Skipping {result_key} - already processed")
            continue
        print("running instance id: ", id)
        # print("code: ", code)
        # print("problem_description: ", problem_description)
        
        # Execute debug agent and get results
        import signal
        import time
        
        # Define timeout handler
        def timeout_handler(signum, frame):
            raise TimeoutError("Debug agent execution timed out after 1 minute")
        
        # Set a timeout of 1 minute (60 seconds)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(60)
        
        try:
            fixed_code, num_turns, conversation = execute_debug_agent(code, problem_description, openai_handler)
            # Cancel the alarm if execution completes successfully
            signal.alarm(0)
        except TimeoutError as e:
            print(f"Timeout: {e}")
            # Reset the alarm and retry
            signal.alarm(0)
            fixed_code, num_turns, conversation = execute_debug_agent(code, problem_description, openai_handler)
            
        # Add the new result
        results[result_key] = {
            "id": id,
            "fixed_code": fixed_code,
            "num_turns": num_turns,
            # "conversation": conversation
        }
        
        # Save updated results
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"Results saved to {results_file}")
        # break
    
    
if __name__ == "__main__":
    main()