import os
import ast
import json

import re

def camel_to_kebab(name):
  """Converts a string from camel case to kebab case."""
  name = re.sub('(?!^)(?=[A-Z])', '-', name)
  return name.lower()

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the test_cases folder
test_cases_dir = os.path.join(current_dir, 'test_cases')

# Get all filenames in the test_cases folder
test_case_files = [f for f in os.listdir(test_cases_dir) if os.path.isfile(os.path.join(test_cases_dir, f))]

tests = [t for t in test_case_files if t.startswith("test")]
solutions = [s for s in test_case_files if s.startswith("q_") and s.endswith(".py")]

test_dicts = []
for test in tests:
    test_id = test.split("_")[2]
    solution = next((s for s in solutions if s.split("_")[1] == test_id), None)
    if solution:
        test_dicts.append({
            "test": os.path.join(test_cases_dir, test),
            "solution": os.path.join(test_cases_dir, solution),
            "id": test_id
        })

def extract_parametrize_cases(test_file_path):
    # Parse the file
    with open(test_file_path, 'r') as file:
        content = file.read()
    
    tree = ast.parse(content)
    
    # Find the test class with parametrize decorator
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Look for the decorator
            for decorator in node.decorator_list:
                if (isinstance(decorator, ast.Call) and 
                    isinstance(decorator.func, ast.Attribute) and 
                    decorator.func.attr == 'parametrize'):
                    
                    try:
                        # Extract parameters
                        # In your structure, args[0] contains param names like "nums, output"
                        # and args[1] contains the list of tuples with test cases
                        param_names = ast.literal_eval(decorator.args[0])
                        param_values = ast.literal_eval(decorator.args[1])
                        
                        # Process each test case
                        test_cases = []
                        for test_case in param_values:
                            # Your test cases are tuples of (input, expected_output)
                            if isinstance(param_names, str):
                                param_names_list = [p.strip() for p in param_names.split(',')]
                            else:
                                param_names_list = param_names
                                
                            if len(param_names_list) != len(test_case):
                                continue
                                
                            test_cases.append({
                                'names': param_names_list,
                                'values': test_case
                            })
                        
                        return node.name, test_cases
                    except Exception as e:
                        print(f"Error parsing parameters: {e}")
                        continue
    
    return None, []

for test_dict in test_dicts:
    test_file_path = test_dict["test"]
    slug_camel = test_file_path.split("/")[-1].split("_")[3].split(".")[0]
    # Convert from camelCase to kebab-case
    slug_kebab = camel_to_kebab(slug_camel)
    test_dict["slug"] = slug_kebab
    class_name, test_cases = extract_parametrize_cases(test_file_path)
    
    if not class_name:
        print(f"No parametrized test class found in {test_file_path}")
        continue
    
    print(f"\nTest file: {os.path.basename(test_file_path)}")
    print(f"Test class: {class_name}")
    print("Test cases:")

    test_lines = []
    
    for i, case in enumerate(test_cases):
        print(f"\nCase {i}:")
        for j, name in enumerate(case['names']):
            print(f"  {name}: {case['values'][j]}")
        
        # Generate the pytest command to run this specific test case
        test_methods = []
        with open(test_file_path, 'r') as file:
            content = file.read()
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == class_name:
                    test_methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef) and m.name.startswith('test_')]
        assert case['names'][-1] == "output"
        output_value = case['values'][-1]

        case['names'] = case['names'][:-1]
        for method in test_methods:
            print(f"    Test line: assert(Solution().{"".join(method.split("_")[1:])}({', '.join([f'{name}={case['values'][j]}' for j, name in enumerate(case['names'])])}) == {case['values'][-1]})")
            test_lines.append(f"assert(Solution().{''.join(method.split('_')[1:])}({', '.join([f'{name}={case['values'][j]}' for j, name in enumerate(case['names'])])}) == {case['values'][-1]})")
    test_dict['test_lines'] = test_lines

print(test_dicts)

test_dicts_dict = {
    test_dict["slug"]: test_dict for test_dict in test_dicts
}

res_files = []
all_combined = []
for filename in os.listdir("res/llama3/debug"):
    if filename.startswith("python") and filename.endswith(".json"):
        filepath = os.path.join("res/llama3/debug", filename)
        with open(filepath, 'r') as f:
            all_combined.extend(json.load(f))

with_dicts = []
for problem in all_combined:
    buggy_code = problem["buggy_code"]
    test_dict = test_dicts_dict.get(problem["slug"])
    if test_dict:
        test_lines = test_dict["test_lines"]
        for line in test_lines:
            buggy_code += f"\n{line}"
        problem["buggy_code"] = buggy_code
        problem["buggy_code"] = "from typing import *\n" + problem["buggy_code"]
        problem["test_dict"] = test_dict
        with_dicts.append(problem)
    else:
        print(f"Test not found for slug: {problem['slug']}")
        continue


for problem in all_combined[:10]:
    print(problem["buggy_code"])


# Save the test_dicts_dict to a JSON file
with open('test_dicts.json', 'w') as f:
    json.dump(test_dicts_dict, f, indent=4)

with open("all_problems_with_cases.json", "w") as f:
    json.dump(with_dicts, f, indent=4)