import os
import sys
import json
import tqdm

from leetcode_oj import LeetCodeTester
from debugger import GPT4Responser, TurboResponser, IOCoder, LiteLLMResponser

SETTING = "code_generation"
MODEL = sys.argv[1]

WORK_DIR = "evaluation"
SRC_DIR = f"dataset_construction/cases"
SAVE_DIR = f"{WORK_DIR}/res/{MODEL}/{SETTING}"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

if MODEL == "llama3":
    responser = LiteLLMResponser(model_name="ollama/llama3:8b-instruct-fp16")
else:
    Responser = {"gpt-4": GPT4Responser, "gpt-35-turbo": TurboResponser}[MODEL]
    responser = Responser()


def load_bug_data():
    """ load data with different languages and bug types """
    res = {
        'cpp': [],
        'java': [],
        'python3': [],
    }
    files = os.listdir(SRC_DIR)
    for file in files:
        file_name = os.path.splitext(file)[0]
        lang = file_name
        res[lang] = json.load(open(os.path.join(SRC_DIR, file)))
    return res


def main():
    responser = Responser()
    coder = IOCoder(responser)
    tester = LeetCodeTester(leetcode_session=os.environ['LEETCODE_SESSION'], csrf_token=os.environ['CSRF_TOKEN'])

    bug_data = load_bug_data()
    for lang in bug_data.keys():

        save_dir = os.path.join(SAVE_DIR, f"{lang}.json")
        if not os.path.exists(save_dir):
            bug_data_split = bug_data[lang]
            res = []

            for case in tqdm.tqdm(bug_data_split, desc=f"{lang}"):
                completed_code = coder.complete(
                    lang=lang,
                    oracle_code=case['oracle_code'],
                    intention=case['description'],
                )
                rw, res_dict = tester.test(code=completed_code, language=lang, task_id=case['slug'])
                case['completed_code'] = completed_code
                case['test_result_bool'] = rw
                case['test_result_dict'] = res_dict
                res.append(case)
                break
            with open(save_dir, 'w') as f:
                json.dump(res, f, indent=4)


if __name__ == '__main__':
    main()
