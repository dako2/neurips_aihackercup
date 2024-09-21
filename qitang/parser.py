from llms import LLM
import re
from app import find_problem


def hard_coded_parsing_tool(full_input_file_path):
    """
    Parses the input file into a list of test cases.

    Parameters:
        full_input_file_path (str): The path to the input file.

    Returns:
        List[List[str]]: A list where each test case is represented as a list of its lines.
    """
    test_cases = []

    with open(full_input_file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    if not lines:
        print("The input file is empty.")
        return test_cases

    try:
        total_test_cases = int(lines[0])
    except ValueError:
        print("The first line of the file should be an integer representing the total number of test cases.")
        return test_cases

    remaining_lines = lines[1:]
    if len(remaining_lines) == total_test_cases:
        # Scenario 1: Each line is a separate test case
        for i, line in enumerate(remaining_lines, start=1):
            test_cases.append([line])  # Each test case is a list with a single string
    else:
        # Scenario 2: Test cases may consist of multiple lines
        index = 0
        test_case_number = 1
        while index < len(remaining_lines) and len(test_cases) < total_test_cases:
            current_line = remaining_lines[index]
            try:
                num_follow_up = int(current_line.split()[0])
            except ValueError:
                print(f"Expected an integer indicating the number of follow-up lines for test case {test_case_number}, but got: '{current_line}'")
                break

            if index + num_follow_up >= len(remaining_lines) + 1:
                print(f"Not enough lines for test case {test_case_number}. Expected {num_follow_up} follow-up lines.")
                break

            # Extract the lines for the current test case
            test_case = remaining_lines[index + 1:index + 1 + num_follow_up]
            test_cases.append(test_case)
            index += 1 + num_follow_up
            test_case_number += 1

    return test_cases
     

def semantic_way_of_parsing():
    llm = LLM('gemini')

    def generate_parsing_prompt(problem_statement):
        # Construct the prompt
        prompt = f"""
    Problem Statement:
    {problem_statement}
    Generate a python code to only parse the input file data by following the input constraint
    **Formatting Instructions: Your response must follow the following xml format.** -
    <source_code>
    def parse_input(input_file): -> List
        ...
        return test_cases
    </source_code>
    """
        return prompt

    def generate_code(prompt):
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

    def main(problem):
        prompt = generate_parsing_prompt(problem.problem_description)
        generated_content = generate_code(prompt)
        if generated_content:
            code = extract_code_from_tags(generated_content)
            code = wrap_code_in_main(code)
            if verify_code_syntax(code):
                with open('generated_parsing_code.py', 'w') as f:
                    f.write(code)
                try:
                    from generated_parsing_code import parse_input
                    test_cases = parse_input(problem.full_input_path)
                except:
                    print('xxx')

try:
    test_cases = hard_coded_parsing_tool('contestData/Fall in Line/sample_in.txt')
    for idx, test_case in enumerate(test_cases, start=1):
        print(f"Test Case {idx}:")
        for line in test_case:
            print(f"  {line}")
except ValueError as ve:
    print(f"Error parsing test cases: {ve}")