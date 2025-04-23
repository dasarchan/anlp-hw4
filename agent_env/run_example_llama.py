import os
import sys
import json
from typing import Dict, List, Any, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_env.llm_agent import LLMDebugAgent
from agent_env.llama3_integration import Llama3Handler, OpenAIHandler

# Example code with a bug
BUGGY_CODE = "from typing import *\n\nclass Solution:\n    '''\n        Test cases walk through \n        Given 7, 4, 9 prove 1, 2                                                            6, 5, 4, 3, 10, prove 2, 3 \n\n        Sort stones -> 4, 7, 9                                                              3, 4, 5, 6, 10 \n        Stone length -> 3                                                                   5\n        Move penultimate = 7 - 4 - 3 + 2 = 2                                                6-3-5+2 = 0 \n        Move final = 9 - 7 - 3 + 2 = 1                                                      10-4-5+2 = 3 \n        Neither is 0, so we cannot return for sure                                          Move penultimate is 0, so move final is assured \n                                                                                            This means we can return [min(2, 3), 3] -> [2, 3]\n\n        Max legal moves is 0                                                                For completeness, max legal moves is 0, max moves is 3  \n        starting index is 0                                                                 starting index is 0 \n\n        Enumeration                                                                         Enumeration\n            index is 0, stone is 4                                                             index is 0, stone is 3 \n            stones[0] lte 4 - 3 ? No, skip while loop                                          stones[0] lte 3 - 5 ? No, skip while \n            max legal moves is min of (max of self and 0 - 0 + 1, most moves)                  max legal moves is min of (max of self and 0 - 0 + 1), max moves -> max legal moves is 1 \n                 -> max legal moves is 1                                                            \n\n            index is 1, stone is 7                                                             index is 1, stone is 4 \n            stones[0] <= 7 - 3 ? Yes, enter while                                              stones[0] lte 4 - 5 ? No, skip while \n                starting index is now 1                                                        max legal moves is min of (max of self and 1 - 0 + 1), max moves -> max legal moves is 2\n            stones[1] <= 7 - 3 ? No, skip while                                                 \n            max legal moves -> min(max of self and 1 - 1 + 1), max_moves \n                -> max legal moves is 1                                                        index is 2, stone is 5 \n                                                                                               stones[0] lte 5 - 5 ? No skip while \n            index is 2, stone is 9                                                             max legal moves is min of (max of self and 2 - 0 + 1), max_moves -> max legal moves is 3 \n            stones[1] <= 9 - 3 ? No, skip while                                                 \n            max legal moves is min(max of self and 2-1 + 1), max_moves\n                 -> max legal moves is 2                                                       index is 3, stone is 6 \n        End enumeration                                                                        stones[0] lte 6 - 5 ? No skip while \n                                                                                               max legal moves is min (max of self and 3 - 0 + 1), max_moves -> max legal moves is 3 \n        Return [3 - 2, 2] -> [1, 2] checks out                                                  \n                                                                                               index is 4, stones is 10 \n                                                                                               stones[0] lte 10 - 5 ? Yes, enter while \n                                                                                                    starting index is 1 \n                                                                                               stones[1] lte 10 - 5 ? Yes, enter while \n                                                                                                    starting index is 2 \n                                                                                               stones[2] lte 10 - 5 ? Yes, enter while \n                                                                                                    starting index is 3 \n                                                                                               max legal moves is min (max of self and 4 - 3 + 1), max moves -> max legal moves is 3 \n                                                                                            End enumeration\n\n                                                                                            Return [5 - 3, 3] -> [2, 3]\n    '''\n    def numMovesStonesII(self, stones: List[int]) -> List[int] :\n        # order does not need to be maintained, so sorting is optimal \n        stones.sort()\n        # want to work within stone physical space since 10^9 >> 10^4 (stone weight vs length)\n        stone_length = len(stones)\n        # what is the cost of moving the second to last stone and the 0th stone? \n        move_penultimate = stones[-2] - stones[0] - stone_length + 2 \n        # what is the cost of moving the last stone and the 1st stone? \n        move_final = stones[-1] - stones[1] - stone_length + 2 \n        # in both of these, the cost is the positional exchange in stones along the stone length + 2 for the two stones moving \n        # our most moves possible are the max of these two \n        most_moves = max(move_penultimate, move_final)\n        # since the stones are unique, if either is 0, the one that we have must be max legal moves \n        # if move penultimate is 0, that means that the second largest stone less the least stone less the length + 2 is 0 \n        # this means that the largest stone, which must be at least one larger than the largest, less the second to least stone which is at least one larger than the least stone  less the length + 2 is move final \n        # our minimal length is 3 \n        # let a, b, c be stones in order \n        # b - a - 3 + 2 = 0 -> b = a + 1 move penultimate  \n        # c - b - 3 + 2 = 0 -> b = c - 1 move final \n        # c - 1 = a + 1 -> c = a + 2 \n        # all stones must be at least 1 to 10^9 and are unique \n        # so at minimum a is 1, b is 2 and c is 3  \n        # in this case, move final is also 0 so we get 0, 0 \n        # if a = 4, b = 5, c = 7 \n        # 5 - 4 - 3 + 2 = 0 move penultimate is 0 \n        # 7 - 5 - 3 + 2 -> 1 move ultimate is 1 \n        # min legal moves is min of 2 and 1 -> min legal moves is 1 -> 1, 1 is returned \n        # from this it can be seen that the movement of c relative to b impacts  the return here when one is 0, and that if either is 0 it does not preclude the other. However it does entail a relation to 2 as most that min could become \n        # this is because if most moves is greater than 2, we could always do the move alternate that was 0 in two steps. This is what locks in to place the ability to use 2 here as the min argument. \n        if move_penultimate == 0 or move_final == 0 : \n            min_legal_moves = min(2, most_moves)\n            return [min_legal_moves, most_moves]\n        # how many legal moves are there in sorted order? \n        max_legal_moves = 0 \n        # starting from 0th index \n        starting_index = 0\n        # enumerate each stone and index \n        for index, stone in enumerate(stones) :\n            # while the stone at starting index is lte this stone minus stone length (cost of a move) \n            while stones[starting_index] <= stone - stone_length : \n            \n            starting_index += 1\n            # max legal moves is then set to maxima of self and indexed difference with 1 for 0 based indexing  \n            max_legal_moves = min(max(max_legal_moves, index - starting_index + 1), most_moves) \n        # return length - max legal moves when in sorted order (your minimal move state) and most moves in sorted order \n        return [stone_length - max_legal_moves, most_moves]\n\nassert(Solution().numMovesStonesII(stones=[7, 4, 9]) == [1, 2])\nassert(Solution().numMovesStonesII(stones=[6, 5, 4, 3, 10]) == [2, 3])"
PROBLEM_DESCRIPTION = "There are some stones in different positions on the X-axis. You are given an integer array stones, the positions of the stones.\nCall a stone an endpoint stone if it has the smallest or largest position. In one move, you pick up an endpoint stone and move it to an unoccupied position so that it is no longer an endpoint stone.\n\nIn particular, if the stones are at say, stones = [1,2,5], you cannot move the endpoint stone at position 5, since moving it to any position (such as 0, or 3) will still keep that stone as an endpoint stone.\n\nThe game ends when you cannot make any more moves (i.e., the stones are in three consecutive positions).\nReturn an integer array answer of length 2 where:\n\nanswer[0] is the minimum number of moves you can play, and\nanswer[1] is the maximum number of moves you can play."


def main():
    llama_handler = Llama3Handler(
        model_name="meta-llama/Meta-Llama-3-8B-Instruct",
        gpu_memory_utilization=0.9,
        max_model_len=8192,
        tensor_parallel_size=1,
        dtype="bfloat16",
        # use_tool_calling=True
    )
    
    # Initialize the LLM Debug Agent
    debug_agent = LLMDebugAgent(
        llm_handler=llama_handler,
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