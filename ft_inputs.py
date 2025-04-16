import openai
import json
import os
from os import listdir
from os.path import isfile, join
import random
import pandas as pd

files = [f for f in listdir("benchmark/") if isfile(join("benchmark/", f))]

buggy_code_examples = [ ]
for file in files:
    if file.startswith("python"):
        with open("benchmark/" + file, "r") as f:
            results = json.load(f)
            for result in results:
                buggy_code_examples.append(result["buggy_code"])

random.seed(100)
buggy_samples = random.sample(buggy_code_examples, 100)

client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://cmu.litellm.ai",
)

prompt = '''
Observe the following buggy Python code. Given pdb console access, please 
generate a list of pdb commands to debug the code. Do not include any explanation.
Output a string in this format:
<pdb command>, <pdb command>, <pdb command>, ...
'''

result_prompts = [ ]
result_inputs = [ ]
result_outputs = [ ]

for sample in buggy_samples:
    buggy_code = f'''
    <code>
    {sample}
    </code>
    '''
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": prompt},
            {"role": "user", "content": buggy_code}
        ],
    )
    pdb_commands = response.choices[0].message.content.split(", ")

    idx = random.sample(range(0, len(pdb_commands)), min(5, len(pdb_commands)))
    for i in idx:
        prev_commands = pdb_commands[:i]
        next_command = pdb_commands[i]

        if i == 0:
            ft_prompt = f'''
            Observe the following buggy Python code. Given pdb console access, please
            output one pdb command to start debugging the code.
            '''

            ft_input = f'''
            <code>
            {sample}
            <\code>
            '''

        else:
            ft_prompt = f'''
            Observe the following buggy Python code and list of pdb commands. 
            Given pdb console access, please output the next pdb command to 
            continue debugging the code.
            '''

            ft_input = f'''
            <code>
            {sample}
            <\code>

            pdb commands: {prev_commands}
            '''
            
        result_prompts.append(ft_prompt)
        result_inputs.append(ft_input)
        result_outputs.append(next_command)


df = pd.DataFrame({"prompt": result_prompts, "input": result_inputs, "output": result_outputs})
df.to_csv("ft_samples.csv", index=False)




