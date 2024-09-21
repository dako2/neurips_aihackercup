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

def setup_logger(debug=False):
    level = "DEBUG" if debug else "INFO"
    logging.basicConfig(
        level=level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )

def check_solution(model_output: str, output: str):
    "A simple check to see if the output is correct"
    # these may be big!
    generated_output = Path(model_output).read_text()
    output = Path(output).read_text()
    return {
        "solved": generated_output.strip() == output.strip(),
        "runnable": model_output,
    }

async def run_python(
    program: Path, input_file: Path,
):
    """
    Run a Python program asynchronously with the given input file and output file,
    logging stderr in a streaming manner.
    """
    timeout: float = 10
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
    evaluation = check_solution(output_file, problem.sample_output_path)

    # Additional information
    if not evaluation["runnable"]:
        logging.error("The submitted code could not be run successfully.")
        return False

    if evaluation["solved"]:
        logging.info("Solution is correct!!!")
        print("Solution is correct!!!")
        return True
    else:
        logging.warning("Solution is incorrect.")
        print("Solution is incorrect.")
        return False

async def evaluate_full_data(problem):

    result = await run_python(problem.code_path, problem.full_input)

    print("complete the running. starting the evaluation...")
    # Check the solution
    evaluation = check_solution(result, problem.full_output)

    # Additional information
    if not evaluation["runnable"]:
        logging.error("The submitted code could not be run successfully.")
        return False

    if evaluation["solved"]:
        logging.info("Solution is correct!!!")
        print("Solution is correct!!!")
        return True
    else:
        logging.warning("Solution is incorrect.")
        print("Solution is incorrect.")
        return False

if __name__ == "__main__":
    main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder
    problem = load_problem_from_folder(main_dir, 1)

    # Execute the asynchronous main function
    asyncio.run(evaluate_sample_data(problem))
