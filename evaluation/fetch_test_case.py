import os
import sys
import json
import tqdm


# dotenv.load_dotenv(dotenv_path='.env')

print("\nLoaded environment variables:")
for key, value in os.environ.items():
    if key.startswith("LEETCODE_") or key.startswith("CSRF_"):
        # Print only first and last few characters for security
        masked_value = value[:10] + "..." + value[-10:] if len(value) > 30 else value
        print(f"{key}: {masked_value}")

SETTING = "debug"

WORK_DIR = "evaluation"
SRC_DIR = f"benchmark"


def load_bug_data():
    """load data with different languages and bug types"""
    res = {
        "cpp": {},
        "java": {},
        "python3": {},
    }
    files = os.listdir(SRC_DIR)
    for file in files:
        file_name = os.path.splitext(file)[0]
        lang = file_name[: file_name.find("_")]
        bug_type = file_name[file_name.find("_") + 1 :]
        res[lang][bug_type] = json.load(open(os.path.join(SRC_DIR, file)))
    return res


bug_data = load_bug_data()
for lang in bug_data.keys():
    for bug_type in bug_data[lang]:
        if lang != "python3":
            continue
        else:
            print(bug_data[lang]["illegal indentation"][0].keys())
            print(bug_data[lang]["illegal indentation"][0]["slug"])
            print(bug_data[lang]["illegal indentation"][0]["examples"])
            


            break
