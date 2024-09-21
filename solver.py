from utils import Problem
from llms import LLM # to pass in LLM object in to make llm calls
import prompts # holds all prompt template
import logging
import re

# TODO to add back image usage

def verify_code_syntax(code_str):
    try:
        compile(code_str, '<string>', 'exec')
        return True
    except SyntaxError as e:
        return False
    
def solve_problem(problem: Problem, model_name: str, use_images=False, timeout=60) -> dict:
    # initiate the LLM objects for llm calling in generate_code
    zero_shot_llm = LLM(model_name=model_name)

    # zero-shot code
    code = generate_code(
        problem,
        zero_shot_llm, 
        system_prompt=prompts.system_prompt, 
        prompt_template=prompts.prompt_template, 
        extract_prompt=prompts.extract_prompt, 
        use_images=use_images)

    input, output = problem.sample_input, problem.sample_output

    problem.code = code

    if verify_code_syntax(code):
        with open(problem.code_path, 'w') as f:
            f.write(code)
        print(f"saved code to {problem.code_path}")
    # below is the evaluate part from prior code that didn't verify yet
    # generated_output = run(code, input=input, timeout=timeout) 
    # return {"code": code, "generated_output": generated_output, "expected_output": output}
        return {"code": code, "code_path": problem.code_path, "problem": problem}
    else:
        return None


# generate_code function to call llm once and generate code solution

def generate_code(
    problem: Problem,
    llm: LLM, 
    system_prompt: str,  # system
    prompt_template: str,  # user
    extract_prompt: str, # prompt to extract code
    use_images: bool = False) -> str:
    logging.info(f"Generating code solution for: {problem.problem_name}")

    problem_prompt = prompt_template.format(
                problem_description=problem.problem_description,
                sample_input=problem.sample_input,
                sample_output=problem.sample_output)
    #print(type(problem_prompt))
    #print(problem_prompt)

    # call model one first time to get the code
    out = llm.run(problem_prompt)
    logging.info("Generating initial analysis and solution")

    # Let's make a second call to the model to extract the code from the response
    extract_code_prompt = extract_prompt.format(output=out)

    # call model second time to extract the code
    solution = llm.run(extract_code_prompt)
    logging.info("Extracting the solution from the previous generation...")

    # further clean-up for corner-case. in case we have ```python stuff...`
    solution = maybe_remove_backticks(solution)

    return solution


# other supportive functions for solve_problems

def maybe_remove_backticks(solution: str) -> str:
    "Remove backticks from the solution"
    solution = solution.strip()
    solution = re.sub(r'^```python\s*', '', solution)
    solution = re.sub(r'\s*```$', '', solution)
    return solution