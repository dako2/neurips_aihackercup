from utils import Problem, load_problem_from_folder
import sys
from solver import solve_problem
import pathlib
import asyncio
import logging
from evaluate import evaluate_sample_data, evaluate_full_data

def main(selected_question): # select one question to load out of 1, 2, 3, 4, 5
    # Step 1: read the folder and load the problems (as a problem (class Problem))
    main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder
    problem = load_problem_from_folder(main_dir, selected_question)

    # Step 2: solver to generate code solution
    solution = solve_problem(problem, model_name="gemini", use_images=False)
    print(solution['code'])
    # Step 3: generate sample_out.txt
    evaluation = asyncio.run(evaluate_sample_data(solution['problem']))
    print(evaluation)

    """
    #Logic :
    While True: #keep reflection
        if evaluation['correction_ratio'] == 1:
            asyncio.run(evaluate_full_data(solution['problem'])) #start evaluate full data
            if not time-out:
                shutil.copy(problem.code_path, problem.best_code_path)
                shutil.copy(problem.full_output, problem.best_full_out_path)
                break
            else: #timeout
                continue
        else:
            if evaluation['correction_ratio'] > problem.best_score:
                copy code to the best code path
                start evaluate full out
                problem.best_score = evaluation['correction_ratio']
            else:
                continue
    """
    # Step 4: generate full_out.txt
    # use threading / subprocess ...
    evaluation = asyncio.run(evaluate_full_data(solution['problem']))

def full_output(selected_question): # select one question to load out of 1, 2, 3, 4, 5
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
        #full_output(selected_question)
    else:
        print("no problems found")

