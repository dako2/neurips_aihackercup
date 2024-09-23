from utils import Problem, load_problem_from_folder
import sys
from solver import solve_problem
import pathlib
import asyncio
import logging
from evaluate_v2 import evaluate_sample_data, evaluate_full_data
import shutil
from score import load_best_scores
import time
main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder

def main(selected_question):  # select one question to load out of 1, 2, 3, 4, 5
    problem = load_problem_from_folder(main_dir, selected_question)
    iteration = 1
    max_iterations = 5  # Adjust as needed to allow multiple attempts

    while iteration <= max_iterations:
        logging.info(f"\n--- Iteration {iteration} ---")
        try:
            solution = solve_problem(problem, model_name="gemini", use_images=False)
            logging.debug(f"Generated solution code:\n{solution['code']}")
        except Exception as e:
            logging.error(f"Error during problem solving: {e}", exc_info=True)
            test_report = "An error occurred while generating the solution. Please check the solver."
            iteration += 1
            continue  # Proceed to the next iteration

        # Step 3: Evaluate the solution against sample data
        evaluation = asyncio.run(evaluate_sample_data(solution['problem']))
        logging.debug(f"Sample evaluation result: {evaluation}")

        # Handle evaluation errors
        if 'error' in evaluation and evaluation['error']:
            if evaluation['error'] == 'Timeout':
                test_report = "The evaluation timed out. Please rewrite the solution with time complexity considerations."
                logging.warning(test_report)
                iteration += 1
                continue  # Proceed to the next iteration
            else:
                test_report = f"An error occurred during evaluation: {evaluation['error']}"
                logging.error(test_report)
                iteration += 1
                continue  # Proceed to the next iteration

        # Extract the correct_ratio for comparison
        correct_ratio = evaluation.get('correct_ratio', 0)
        logging.info(f"Correct Ratio: {correct_ratio*100:.2f}% ({evaluation.get('correct_count', 0)}/{evaluation.get('total_cases', 0)})")

        # Check if the current solution is better than the best score
        if correct_ratio > problem.best_score:
            try:
                if problem.best_code_path.exists():
                    backup_path = problem.best_code_path.with_suffix('.%d'%(int(time.time())))
                    shutil.copy2(problem.best_code_path, backup_path)
                    logging.info(f"Existing best code backed up to {backup_path}")
                # Update the best solution code
                shutil.copy(problem.code_path, problem.best_code_path)
                logging.info(f"New best score achieved: {correct_ratio*100:.2f}%. Updated best code path to {problem.best_code_path}")

                # Update problem's best score and best code path
                problem.best_score = correct_ratio
                problem.best_code_path = problem.code_path
            except Exception as e:
                logging.error(f"Error while copying best code: {e}", exc_info=True)
                test_report = "Failed to update the best solution code."
                iteration += 1
                continue  # Proceed to the next iteration

            # If the solution is perfect, evaluate against full data
            if correct_ratio == 1.0:
                full_evaluation = asyncio.run(evaluate_full_data(solution['problem']))
                logging.debug(f"Full data evaluation result: {full_evaluation}")

                # Handle full data evaluation errors
                if 'error' in full_evaluation and full_evaluation['error']:
                    if full_evaluation['error'] == 'Timeout':
                        test_report = "The solution is correct, however the full data evaluation timed out. Please rewrite the solution with time complexity considerations."
                        logging.warning(test_report)
                        iteration += 1
                        continue  # Proceed to the next iteration
                    else:
                        test_report = f"An error occurred during full data evaluation: {full_evaluation['error']}"
                        logging.error(test_report)
                        iteration += 1
                        continue  # Proceed to the next iteration

                # If full data evaluation is successful, update best full output path and exit loop
                try:
                    if problem.best_full_out_path.exists():
                        backup_path = problem.best_full_out_path.with_suffix('.%d'%(int(time.time())))
                        shutil.copy2(problem.best_full_out_path, backup_path)
                        logging.info(f"Existing best code backed up to {backup_path}")

                    shutil.copy(problem.full_output, problem.best_full_out_path)
                    logging.info(f"Full output copied to {problem.best_full_out_path}")
                    problem.best_full_out_path = problem.full_output
                    logging.info("Perfect solution found and full data evaluated successfully. Exiting loop.")
                    break  # Exit the loop as a perfect solution has been found
                except Exception as e:
                    logging.error(f"Error while copying full output: {e}", exc_info=True)
                    test_report = "Failed to update the best full output."
                    iteration += 1
                    continue  # Proceed to the next iteration
            else:
                # If the solution is better but not perfect, continue to the next iteration
                logging.info("Improved solution found, continuing to next iteration for further optimization.")
                iteration += 1
                continue

        else:
            # Current solution is not better than the best score
            test_report = "Current solution is worse than before. Please revisit the problem and provide a better solution."
            logging.warning(test_report)
            iteration += 1
            continue  # Proceed to the next iteration

    logging.info("Evaluation process completed.")

def generate_full_output_only(selected_question): # select one question to load out of 1, 2, 3, 4, 5
    # Step 1: read the folder and load the problems (as a problem (class Problem))
    main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder
    
    problem = load_problem_from_folder(main_dir, selected_question)
    asyncio.run(evaluate_sample_data(problem))
    asyncio.run(evaluate_full_data(problem))

#check the solution correction ratio
#if the correction ratio is higher, then override the file in to_submit folder
#else just keep running

if __name__=="__main__":
    if len(sys.argv) > 1:
        selected_question = int(sys.argv[1])
        main(selected_question)
    else:
        print("app.py [question number]")

