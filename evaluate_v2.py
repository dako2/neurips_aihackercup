from dataclasses import dataclass
import pathlib
import asyncio
import logging
from pathlib import Path
import sys
import os
import shutil
from typing import Optional

from rich.logging import RichHandler
from utils import load_problem_from_folder

@dataclass
class RunResult:
    success: bool
    timeout: bool
    error: Optional[str]
    output_file: Optional[Path]

def check_solution(model_output_path: str, expected_output_path: str):
    """
    Compare the generated output with the expected output.

    Parameters:
        model_output_path (str): Path to the generated output file.
        expected_output_path (str): Path to the expected output file.

    Returns:
        dict: Contains 'solved' (bool) and 'runnable' (str).
    """
    try:
        generated_output = Path(model_output_path).read_text()
    except Exception as e:
        logging.error(f"Failed to read generated output file: {e}")
        return {
            "solved": False,
            "runnable": model_output_path,
        }

    try:
        expected_output = Path(expected_output_path).read_text()
    except Exception as e:
        logging.error(f"Failed to read expected output file: {e}")
        return {
            "solved": False,
            "runnable": model_output_path,
        }

    return {
        "solved": generated_output.strip() == expected_output.strip(),
        "runnable": model_output_path,
    }

def setup_logger(debug=False):
    """
    Configure the logger with RichHandler and FileHandler.

    Parameters:
        debug (bool): If True, set logging level to DEBUG.
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[
            RichHandler(),
            logging.FileHandler("evaluation.log"),
        ]
    )

def calculate_correct_ratio_from_files(expected_file_path: str, actual_file_path: str):
    """
    Calculate the ratio of correct cases by comparing expected and actual output files.

    Parameters:
        expected_file_path (str): Path to the expected output file.
        actual_file_path (str): Path to the actual output file.

    Returns:
        dict: Contains 'solved', 'correct_ratio', 'correct_count', 'total_cases', and optionally 'error'.
    """
    # Read the expected output file
    try:
        with open(expected_file_path, 'r') as f:
            expected_output = f.read()
    except Exception as e:
        logging.error(f"Failed to read expected output file: {e}")
        return {
            'solved': False,
            'correct_ratio': 0,
            'correct_count': 0,
            'total_cases': 0,
            'error': 'Failed to read expected output file'
        }

    # Split the expected and actual outputs into lists
    expected_cases = expected_output.strip().split("\n")

    try:
        # Read the actual output file
        with open(actual_file_path, 'r') as f:
            actual_output = f.read()
        actual_cases = actual_output.strip().split("\n")
    except Exception as e:
        logging.error(f"Failed to read actual output file: {e}")
        return {
            'solved': False,
            'correct_ratio': 0,
            'correct_count': 0,
            'total_cases': len(expected_cases),
            'error': 'Failed to read actual output file'
        }

    # Ensure both lists have the same length
    if len(expected_cases) != len(actual_cases):
        logging.warning("Mismatch in the number of cases")
        return {
            'solved': False,
            'correct_ratio': 0,
            'correct_count': 0,
            'total_cases': len(expected_cases),
            'error': 'Mismatch in the number of cases'
        }

    correct_count = 0
    for idx, (e, a) in enumerate(zip(expected_cases, actual_cases), start=1):
        if e == a:
            logging.info(f"Case {idx}: Correct")
            correct_count += 1
        else:
            logging.warning(f"Case {idx}: Mismatch - Expected: '{e}', Got: '{a}'")

    total_cases = len(expected_cases)
    correct_ratio = correct_count / total_cases if total_cases > 0 else 0

    return {
        'solved': correct_ratio == 1.0,
        'correct_ratio': correct_ratio,
        'correct_count': correct_count,
        'total_cases': total_cases
    }

async def run_python(program: Path, input_file: Path) -> RunResult:
    """
    Run a Python program asynchronously with the given input file and output file,
    logging stderr in a streaming manner.

    Parameters:
        program (Path): Path to the Python program to execute.
        input_file (Path): Path to the input file.

    Returns:
        RunResult: Result of the execution containing success status, timeout flag,
                   error message, and output file path.
    """
    timeout: float = 30.0  # Timeout in seconds
    suffix: str = "_generated_output.txt"

    output_file = input_file.parent / f"{input_file.stem}{suffix}"
    process = None  # Declare process outside try-except to handle timeout properly

    try:
        program = program.resolve()
        input_path = input_file.resolve()
        output_path = output_file.resolve()

        if not program.is_file():
            error_msg = f"Program file not found: {program}"
            logging.error(error_msg)
            return RunResult(success=False, timeout=False, error=error_msg, output_file=None)

        if not input_file.is_file():
            error_msg = f"Input file not found: {input_file}"
            logging.error(error_msg)
            return RunResult(success=False, timeout=False, error=error_msg, output_file=None)

        with input_file.open("rb") as infile, output_file.open("wb") as outfile:
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                str(program),
                stdin=infile,
                stdout=outfile,
                stderr=asyncio.subprocess.PIPE,
            )

            async def read_stderr():
                # Async streaming of stderr
                async for line in process.stderr:
                    if line:
                        logging.error(line.decode().strip())

            try:
                # Run both tasks concurrently with timeout
                await asyncio.wait_for(
                    asyncio.gather(
                        read_stderr(),
                        process.wait(),
                    ),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()  # Kill the process if timeout occurs
                await process.wait()  # Ensure the process is cleaned up to avoid zombie process
                error_msg = f"Program execution timed out after {timeout} seconds"
                logging.error(error_msg)
                return RunResult(success=False, timeout=True, error=error_msg, output_file=None)

            if process.returncode != 0:
                error_msg = f"Program execution failed with return code {process.returncode}"
                logging.error(error_msg)
                return RunResult(success=False, timeout=False, error=error_msg, output_file=None)

            logging.info(f"Output saved to {output_path}")
            return RunResult(success=True, timeout=False, error=None, output_file=output_file)

    except Exception as e:
        error_msg = f"Error running Python program: {e}"
        logging.error(error_msg, exc_info=True)
        return RunResult(success=False, timeout=False, error=error_msg, output_file=None)

async def evaluate_sample_data(problem):
    """
    Evaluate the user solution against the sample data.

    Parameters:
        problem (Problem): An instance containing paths to the code, sample input, and sample output.

    Returns:
        dict: Evaluation results including 'solved', 'correct_ratio', 'correct_count', 'total_cases', and optionally 'error'.
    """
    try:
        result = await run_python(problem.code_path, problem.sample_input_path)

        if result.timeout:
            logging.warning("Sample data evaluation timed out.")
            return {
                'solved': False,
                'correct_ratio': 0,
                'correct_count': 0,
                'total_cases': 0,
                'error': 'Timeout'
            }

        if not result.success:
            logging.warning(f"Sample data evaluation failed: {result.error}")
            return {
                'solved': False,
                'correct_ratio': 0,
                'correct_count': 0,
                'total_cases': 0,
                'error': result.error
            }

        # Check the solution
        evaluation = calculate_correct_ratio_from_files(problem.sample_output_path, str(result.output_file))

        if evaluation.get("solved", False):
            logging.info("Sample solution is correct!!!")
        else:
            logging.warning("Sample solution is incorrect.")

        logging.info(f"Correct Ratio: {evaluation.get('correct_ratio', 0)*100:.2f}% ({evaluation.get('correct_count', 0)}/{evaluation.get('total_cases', 0)})")
        return evaluation

    except Exception as e:
        logging.error(f"Failed to evaluate sample data: {e}", exc_info=True)
        return {
            'solved': False,
            'correct_ratio': 0,
            'correct_count': 0,
            'total_cases': 0,
            'error': str(e)
        }

async def evaluate_full_data(problem):
    """
    Evaluate the user solution against the full data.

    Parameters:
        problem (Problem): An instance containing paths to the code, full input, and full output.

    Returns:
        dict: Evaluation results including 'solved', 'correct_ratio', 'correct_count', 'total_cases', and optionally 'error'.
    """
    logging.info("Running full data evaluation...")
    try:
        result = await run_python(problem.code_path, problem.full_input)

        if result.timeout:
            logging.warning("Full data evaluation timed out.")
            return {
                'solved': False,
                'correct_ratio': 0,
                'correct_count': 0,
                'total_cases': 0,
                'error': 'Timeout'
            }

        if not result.success:
            logging.warning(f"Full data evaluation failed: {result.error}")
            return {
                'solved': False,
                'correct_ratio': 0,
                'correct_count': 0,
                'total_cases': 0,
                'error': result.error
            }

        # Check the solution
        evaluation = calculate_correct_ratio_from_files(problem.full_output_path, str(result.output_file))

        if evaluation.get("solved", False):
            logging.info("Full data solution is correct!!!")
        else:
            logging.warning("Full data solution is incorrect.")

        logging.info(f"Correct Ratio: {evaluation.get('correct_ratio', 0)*100:.2f}% ({evaluation.get('correct_count', 0)}/{evaluation.get('total_cases', 0)})")
        return evaluation

    except Exception as e:
        logging.error(f"Failed to evaluate full data: {e}", exc_info=True)
        return {
            'solved': False,
            'correct_ratio': 0,
            'correct_count': 0,
            'total_cases': 0,
            'error': str(e)
        }
