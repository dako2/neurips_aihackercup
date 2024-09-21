from dataclasses import dataclass
import simple_parsing
import pathlib
import asyncio
import logging
from pathlib import Path
import sys
import os
from pydantic import BaseModel, Field
from rich.logging import RichHandler
from utils import load_problem_from_folder

def check_solution(model_output: str, output: str):
    "A simple check to see if the output is correct"
    # these may be big!
    generated_output = Path(model_output).read_text()
    output = Path(output).read_text()
    return {
        "solved": generated_output.strip() == output.strip(),
        "runnable": model_output,
    }

def setup_logger(debug=False):
    level = "DEBUG" if debug else "INFO"
    logging.basicConfig(
        level=level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )

def calculate_correct_ratio_from_files(expected_file_path: str, actual_file_path:str):
    # Read the expected output file
    with open(expected_file_path, 'r') as f:
        expected_output = f.read()
    # Split the expected and actual outputs into lists
    expected_cases = expected_output.strip().split("\n")

    try:
        # Read the actual output file
        with open(actual_file_path, 'r') as f:
            actual_output = f.read()
        actual_cases = actual_output.strip().split("\n")
    except:
        print("no actual cases")
        return {'solved': False, 'correct_ratio': 0, 'correct_count': 0, 'total_cases': len(actual_cases)}

    # Ensure both lists have the same length
    if len(expected_cases) != len(actual_cases):
        print("Mismatch in the number of cases")
        return {'solved': False, 'correct_ratio': 0, 'correct_count': 0, 'total_cases': len(actual_cases)}

    for e, a in zip(expected_cases, actual_cases):
        if e == a:
            print(f"Correct: {e} == {a}")
        else:
            print(f"Mismatch: expected {e}, got {a}")

    # Count the number of correct cases
    correct_count = sum(1 for e, a in zip(expected_cases, actual_cases) if e == a)
    total_cases = len(expected_cases)
    correct_ratio = correct_count / total_cases

    return {'solved': True, 'correct_ratio': correct_ratio, 'correct_count': correct_count, 'total_cases': total_cases}

async def run_python(
    program: Path, input_file: Path,
):
    """
    Run a Python program asynchronously with the given input file and output file,
    logging stderr in a streaming manner.
    """
    timeout: float = 30
    suffix: str = "_generated_output.txt"

    output_file = Path(input_file).parent / (Path(input_file).stem + suffix)
    process = None  # Declare process outside try-except to handle timeout properly
    try:
        program = str(program)
        input_path = str(input_file)
        output_path = str(output_file)

        with input_file.open("rb") as infile, output_file.open("wb") as outfile:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                program,
                stdin=infile,
                stdout=outfile,
                stderr=asyncio.subprocess.PIPE,
            )

            async def read_stderr():
                # Async streaming of stderr
                async for line in process.stderr:
                    if line:
                        logging.error(line.decode().strip())

            # Run both tasks concurrently
            await asyncio.wait_for(
                asyncio.gather(
                    read_stderr(),
                    process.wait(),
                ),
                timeout=timeout
            )

            if process.returncode != 0:
                raise RuntimeError(f"Program execution failed with return code {process.returncode}")

            logging.info(f"Output saved to {output_path}")

    except asyncio.TimeoutError:
        if process:
            process.kill()  # Kill the process if timeout occurs
            await process.wait()  # Ensure the process is cleaned up to avoid zombie process
        raise TimeoutError(f"Program execution timed out after {timeout} seconds")
    except Exception as e:
        logging.error(f"Error running Python program: {e}", exc_info=True)
        raise RuntimeError(f"Error running Python program: {str(e)}")
    return output_file

async def evaluate_sample_data(problem):

    output_file = await run_python(problem.code_path, problem.sample_input_path)
    # Check the solution
    evaluation_0 = check_solution(output_file, problem.sample_output_path)
    evaluation = calculate_correct_ratio_from_files(problem.sample_output_path, output_file)

    if evaluation_0["solved"]:
        logging.info("Solution is correct!!!")
        print("Solution is correct!!!")
        return evaluation
    else:
        logging.warning("Solution is incorrect.")
        print("Solution is incorrect.")
        return evaluation

async def evaluate_full_data(problem):
    print("running evaluation...")
    result = await run_python(problem.code_path, problem.full_input)

if __name__ == "__main__":
    main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder
    problem = load_problem_from_folder(main_dir, 1)

    # Execute the asynchronous main function
    asyncio.run(evaluate_sample_data(problem))
