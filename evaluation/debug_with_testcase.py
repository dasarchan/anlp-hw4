import os
import sys
import json
from tqdm import tqdm
import dotenv

from leetcode_oj import LeetCodeTester, LeetCodeTesterPool
from debugger import GPT4Responser, TurboResponser, IODebugger, LiteLLMResponser

# dotenv.load_dotenv(dotenv_path='.env')

print("\nLoaded environment variables:")
for key, value in os.environ.items():
    if key.startswith("LEETCODE_") or key.startswith("CSRF_"):
        # Print only first and last few characters for security
        masked_value = value[:10] + "..." + value[-10:] if len(value) > 30 else value
        print(f"{key}: {masked_value}")

SETTING = "debug"
MODEL = sys.argv[1]

WORK_DIR = "evaluation"
SRC_DIR = f"benchmark"
SAVE_DIR = f"{WORK_DIR}/res/{MODEL}_with_testcase/{SETTING}"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Responser = {'gpt-4': GPT4Responser, 'gpt-35-turbo': TurboResponser}[MODEL]
if MODEL == "llama3":
    responser = LiteLLMResponser(model_name="ollama/llama3:8b-instruct-fp16")
elif MODEL == "deepseek-coder:33b":
    responser = LiteLLMResponser(model_name="ollama/deepseek-coder:33b")
else:
    Responser = {"gpt-4": GPT4Responser, "gpt-35-turbo": TurboResponser}[MODEL]
    responser = Responser()


def main():
    
    
    test_cases = json.load(
        open(
            "/Users/zhijie/Documents/11-711 Advanced NLP/anlp-hw4/debug_results_with_testcases.json"
            # "/Users/zhijie/Documents/11-711 Advanced NLP/anlp-hw4/agent_env/debug_results.json"
        )
    )
    print(len(test_cases))
    for _, test_info in test_cases.items():
        print(test_info['id'][0])
        print(test_info['id'][1])
        print(test_info['fixed_code'])
        break
    # debugger = IODebugger(responser)
    # Replace single tester with a tester pool
    leetcode_sessions = [os.environ['LEETCODE_SESSION']]
    csrf_tokens = [os.environ['CSRF_TOKEN']]
    
    tester_pool = LeetCodeTesterPool(leetcode_sessions=leetcode_sessions, csrf_tokens=csrf_tokens)

    # tester = LeetCodeTester(leetcode_session=os.environ['LEETCODE_SESSION'], csrf_token=os.environ['CSRF_TOKEN'])
    # bug_data = load_bug_data()
    
    lang = "python3"
    save_dir = os.path.join(SAVE_DIR, f"debug_result.json")
    if os.path.exists(save_dir):
        with open(save_dir, "r") as f:
            res = json.load(f)
    else:
        res = []
    unique_ids = set([test_info['unique_id'] for test_info in res])
    for test_id, test_info in tqdm(test_cases.items(), desc="Processing test cases"):
        if test_id in unique_ids:
            print(f"Test case {test_id} already exists")
            continue
        else:
            fixed_code = test_info['fixed_code']
            # if "assert(" in fixed_code:
            #     fixed_code = fixed_code[:fixed_code.find("assert(")]
            
            # print(fixed_code)
            rw, res_dict = tester_pool.test(
                code=fixed_code, language=lang, task_id=test_info['id'][0]
            )
            test_info["unique_id"] = test_id
            test_info["fixed_code"] = fixed_code
            # case['fixing_exp'] = fixing_exp
            test_info["test_result_bool"] = rw
            test_info["test_result_dict"] = res_dict
            res.append(test_info)
        # break
        with open(save_dir, "w") as f:
            json.dump(res, f, indent=4)


if __name__ == '__main__':
    main()
