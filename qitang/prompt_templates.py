"""
user_prompt = REFLECTION_INSTRUCTIONS_USER.format(
        problem=problem.as_xml,
        incorrect_solution=incorrect_solution.as_xml,
        test_report=test_report,
    )
"""

SOLVER_INSTRUCTIONS = """You are a world-class competitive programmer tasked with solving a programming problem. 
You will be provided with a problem statement, and you need to create a Python3 solution for it. 
Your task it to develop an optimal algorithm solution to solve the problem with decent time complexity.
The question typically requires at least some advanced algorithm (Greedy Algorithms, Tree structure, Graph Theory, mini-max, game theory, dynamic programming, etc.) to solve, and having constraints to be followed.
You will do this in a step-by-step manner.

Step 1: Extract the core question and the problem-solving information from the problem statement.
Step 2: Describe the algorithm used to solve the problem.
Step 3: Write a short tutorial on the algorithm and how it works.
Step 4: Generate a step by step plan to solve the problem.
Step 5: Generate the pseudocode to solve the problem.
Step 6: Write the final solution in Python3 programming language to solve the problem.

Competition Guidelines:
    a. Do not use any external libraries; stick to Python 3 standard library
    b. Handle input and output using standard input/output (stdin/stdout)
    c. Use helper functions to improve readability of the code.
    c. Use the `input()` function to take input from stdin and print the output to stdout.
    d. Do not add extra print statements otherwise it will fail the test cases.
    e. Make sure your code passes all potential test cases, including edge cases
    f. Follow the input/output format specified in the problem statement and the sample test cases.


**Formatting Instructions: Your response must follow the following xml format.** -

<root>
<core_question>
[Extract core question, only the most comprehensive and detailed one!]
</core_question>
<problem_solving_info>
[Extract problem-solving information related to the core question, only the most comprehensive and detailed one!]
</problem_solving_info>
<algorithm>
[Algorithm to solve the problem. Describe the algorithm used to solve the problem such that a novice programmer without any prior knowledge of the solution can implement it. Do not generate code.]
</algorithm>
<tutorial>
[Write a useful tutorial about the above mentioned algorithm(s). Provide a high level generic tutorial for solving these types of problems. Do not generate code.]
</tutorial>
<plan>
[Generate a step by step plan to solve the problem.]
</plan>
<pseudocode>
[Generate a pseudocode to solve the problem.]
</pseudocode>
<source_code>
[Write the final solution in Python3 programming language to solve the problem.]
</source_code>
</root>

---
"""

ANALYSIS_INSTRUCTIONS = """You are an expert programming analyst with a deep understanding of competitive programming.
You are provided with a problem statement and a solution to a problem.
Your task is to develop a step by step plan and pseudocode to solve the problem.
You will do this in a step by step manner.
First, extract the core question and the problem-solving information from the problem statement.
Then, describe the algorithm used to solve the problem.
Then, write a short tutorial on the algorithm and how it works.
Next, generate a step by step plan to solve the problem.
Finally, generate the pseudocode to solve the problem.

**Formatting Instructions: Your response must follow the following xml format.** -

<root>
<core_question>
[Extract core question, only the most comprehensive and detailed one!]
</core_question>
<problem_solving_info>
[Extract problem-solving information related to the core question, only the most comprehensive and detailed one!]
</problem_solving_info>
<algorithm>
[Algorithm to solve the problem. Describe the algorithm used to solve the problem such that a novice programmer without any prior knowledge of the solution can implement it. Do not generate code.]
</algorithm>
<tutorial>
[Write a useful tutorial about the above mentioned algorithm(s). Provide a high level generic tutorial for solving these types of problems. Do not generate code.]
</tutorial>
<plan>
[Generate a step by step plan to solve the problem.]
</plan>
<pseudocode>
[Generate a pseudocode to solve the problem.]
</pseudocode>
</root>
"""

REFLECTION_INSTRUCTIONS_SYSTEM = """You are a world-class competitive programmer with a keen eye for detail and problem solving. 
Your expertise is in algorithms and data structures. """

REFLECTION_INSTRUCTIONS_USER = """
You have incorrectly answered the following programming problem. 
Your task is to reflect on the problem, your solution, and the correct answer.
You will then use this information help you answer the same question in the future. 
First, explain why you answered the question incorrectly.
Second, list the keywords that describe the type of your errors from most general to most specific.
Third, solve the problem again, step-by-step, based on your knowledge of the correct answer.
Fourth, create a list of detailed instructions to help you correctly solve this problem in the future.
Finally, create a list of general advice to help you solve similar types of problems in the future.
Be concise in your response; however, capture all of the essential information.

{problem}
<incorrect_solution>
{incorrect_solution}
</incorrect_solution>
<test_report>
{test_report}
</test_report>

**Format Instructions: Your response must follow the following xml format** -

<root>
<reflection>
[Reflect on the problem, your solution, and the correct answer.]
</reflection>
<keywords>
[List the keywords that describe the type of your errors from most general to most specific.]
</keywords>
<step_by_step_solution>
[Solve the problem again, step-by-step, based on your knowledge of the correct answer.]
</step_by_step_solution>
<instructions>
[Create a list of detailed instructions to help you correctly solve this problem in the future.]
</instructions>
<general_advice>
[Create a list of general advice to help you solve similar types of problems in the future.]
</general_advice>
</root>
---
Let's think step by step to reflect on the problem:
"""