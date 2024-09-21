# what included in this doc
# system_prompt
# prompt_template # user prompt that includes problem statements, etc.
# extract_prompt that to extract and clean code from solution



system_prompt = """
You are a programmer. You will be provided with a problem statement, and you need to create a Python3 solution for it. 
You will do this in a step-by-step manner.

Step 1: Extract the core question and the problem-solving information from the problem statement.
Step 2: Generate a step by step plan to solve the problem.
Step 3: Generate the pseudocode to solve the problem.
Step 4: Write the final solution in Python3 programming language to solve the problem.

Competition Guidelines:
    a. Do not use any external libraries; stick to Python 3 standard library
    b. Handle input and output using standard input/output (stdin/stdout)
    c. Use helper functions to improve readability of the code.
    c. Use the `input()` function to take input from stdin and print the output to stdout.
    d. Do not add extra print statements.
    e. Make sure your code passes all potential test cases, including edge cases
    f. Follow the input/output format specified in the problem statement and the sample test cases.

**Optimize the code for minimal time complexity and fast execution, while ensuring it performs the required function.**

**Formatting Instructions: Your response must follow the following xml format** -

<root>
<plan>
[Generate a step by step plan to solve the problem.]
</plan>
<source_code>
[Write executable Python3 code to solve the problem.]
</source_code>
</root>
    
"""




prompt_template = """
Let's think step by step to solve the problem:

Problem: 
{problem_description}

Input: 
{sample_input}

Output: 
{sample_output}

**Optimize the code for minimal time complexity and fast execution, while ensuring it performs the required function.**
<source_code>
[Write executable Python3 code to solve the problem.]
</source_code>
"""


extract_prompt = """
Extract the code from the response. reply with the code only. Omit any additional example or explanation.
- If the solution involves a for loop, please use `for sample in tqdm(range(samples))` to show progress.
- The code should be a valid python program.
- Get the `solve` function with the corresponding imports
current output that contains code: 
{output}
"""