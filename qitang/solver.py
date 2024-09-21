from llms import LLM
import re
from app import find_problem
from prompt_templates import SOLVER_INSTRUCTIONS, REFLECTION_INSTRUCTIONS_USER

llm = LLM('gemini')

def generate_parsing_prompt(problem_statement):
    # Construct the prompt
    prompt = SOLVER_INSTRUCTIONS + f"""
<problem_description>
{problem_statement}
</problem_description>
<instruction>
Generate a python code to only parse the input file data by following the input constraint
**Formatting Instructions: Your response must follow the following xml format.** -
</instruction>
<source_code>
def main():
    # the generated source code to solve the problems in python3
    # do not use any external library
    # do not use threading
    # Strictly follow the input and output formats given in the problem statement
    return
</source_code>
"""
    return prompt

def generate_response(prompt):
    # Prepare the messages for the model
    response = llm.run(prompt)
    # Check if the response is valid
    if response:
        cleaned_code = remove_code_fences(response)
        return cleaned_code.strip()
    else:
        return None

def extract_code_from_tags(text):
    """
    Extracts the code enclosed within <source_code> and </source_code> tags.
    """
    pattern = r'<source_code>(.*?)</source_code>'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        code = match.group(1).strip()
        return code
    else:
        return text
    
def remove_code_fences(code_text):
    """
    Removes various code fences and unnecessary headers from the code.
    """
    code_text = code_text.strip()
    
    # Patterns to remove
    code_fence_patterns = [
        r"^```[\w]*\n",        # ``` or ```python\n at the start
        r"^'''[\w]*\n",        # ''' or '''python\n at the start
        r"^\"\"\"[\w]*\n",     # """ or """python\n at the start
        r"\n```$",             # ``` at the end
        r"\n'''$",             # ''' at the end
        r"\n\"\"\"$",          # """ at the end
    ]
    
    for pattern in code_fence_patterns:
        code_text = re.sub(pattern, '', code_text, flags=re.MULTILINE)
     
    return code_text

def verify_code_syntax(code_str):
    try:
        compile(code_str, '<string>', 'exec')
        return True
    except SyntaxError as e:
        return False

def verify_file_syntax(file_path):
    try:
        with open(file_path, 'r') as f:
            code_str = f.read()
        return verify_code_syntax(code_str)
    except FileNotFoundError:
        return False

def wrap_code_in_main(code_text):
    """
    Wraps the given code inside a main() function and adds the if __name__ == "__main__": block.
    """
    import textwrap
    indented_code = textwrap.indent(code_text, '    ')
    main_code = f"def main():\n{indented_code}\n\nif __name__ == \"__main__\":\n    main()"
    return main_code

def read_code(file_path):
    with open(file_path, 'r') as f:
        return f.read()

if __name__ == "__main__":   

    #for i in range(1,6): 
    for i in [1]:
        problem = find_problem(i)
        prompt = generate_parsing_prompt(problem.problem_description)
        generated_content = generate_response(prompt)

        if generated_content:
            code = extract_code_from_tags(generated_content)

            if verify_code_syntax(code):
                with open('to_submit/%s.py'%problem.problem_name, 'w') as f:
                    f.write(code)
                print(code)