from pydantic import BaseModel, Field
import pathlib
import re

class Problem(BaseModel):
    problem_dir: pathlib.Path = Field(
        ..., description="The path to the problem directory"
    )
    problem_name: str = Field(..., description="The name of the problem")
    problem_description: str = Field(..., description="The description of the problem")
    sample_input: str = Field(..., description="The sample input of the problem")
    sample_output: str = Field(..., description="The sample output of the problem")
    sample_input_path: pathlib.Path = Field(..., description="The sample input path of the problem")
    sample_output_path: pathlib.Path = Field(..., description="The sample output path of the problem")
    full_input: pathlib.Path = Field(..., description="The path to the input file")
    full_output: pathlib.Path = Field(..., description="The path to the output file")
    code_path: pathlib.Path = Field(..., description="The path to the output code file")
    code: str = Field(..., description="The generated source code")
    best_score: int = Field(..., description="The best score of the solution")
    best_code_path: pathlib.Path = Field(..., description="The path to the output code file")
    best_full_out_path: pathlib.Path = Field(..., description="The path to the output code file")
    @property
    def as_xml(self) -> str:
        return f"""
<problem>
<problem_statement>
{remove_extra_newlines(self.problem_description)}
</problem_statement>
<sample_test_cases>
<sample_input>
{self.sample_input}
</sample_input>
<sample_output>
{self.sample_output}
</sample_output>
</sample_test_cases>
</problem>
"""

# problem_dir: ./contestData/Fall_in_line
# problem_name: Fall_in_line
def load_problem(problem_name: str, problem_dir: pathlib.Path) -> Problem:
    full_input = problem_dir / f"full_in.txt"
    full_output = problem_dir / f"full_in_generated_output.txt" # to add timestamp
    sample_input_path = problem_dir / f"sample_in.txt"
    sample_output_path = problem_dir / f"sample_out.txt"
    problem_description = problem_dir / f"statement.txt"
    code_path = problem_dir / f"{problem_name}.py"
    best_score = 0.0
    best_code_path  =  f"to_submit/{problem_name}.py"
    best_full_out_path = f"to_submit/{problem_name}_full_out.txt"
    return Problem(
        problem_dir=problem_dir,
        problem_name=problem_name,
        problem_description=problem_description.read_text(),
        sample_input=sample_input_path.read_text(),
        sample_output=sample_output_path.read_text(),
        sample_input_path = sample_input_path,
        sample_output_path = sample_output_path,
        full_input=full_input,
        full_output=full_output, # to generate
        code_path = code_path,
        code = '',
        best_score = best_score,
        best_code_path = best_code_path,
        best_full_out_path = best_full_out_path,
    )

def load_problem_from_folder(main_dir_path: str, selected_question: int) -> Problem:
    """
    Reads the main directory, selects the specified question, and returns the corresponding Problem object.
    
    :param main_dir_path: Path to the main directory containing subfolders with problems
    :param selected_question: Index (1-based) of the question to load
    :return: An instance of the Problem class
    """
    # Step 1: Define the main directory
    main_dir = pathlib.Path(main_dir_path)
    
    # Step 2: Get the list of subfolder names, replacing spaces with underscores
    sub_problem_dir = [f.name for f in main_dir.iterdir() if f.is_dir()]
    
    # Step 3: Select the specific problem based on the index
    if 0 < selected_question <= len(sub_problem_dir):
        problem_name = sub_problem_dir[selected_question - 1]
        problem_dir = main_dir / problem_name
        
        # Step 4: Load and return the selected problem
        problem = load_problem(problem_name, problem_dir)
        print(problem.problem_name)
        return problem
    else:
        raise IndexError(f"Selected question index {selected_question} is out of range. Must be between 1 and {len(sub_problem_dir)}.")


def remove_extra_newlines(text: str) -> str:
    # Use regex to replace 2 or more newlines (with possible whitespace in between) with a single newline
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text
