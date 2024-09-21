from utils import Problem, load_problem_from_folder
import sys
import pathlib

main_dir = pathlib.Path("./contestData")

def find_problem(selected_question): # select one question to load out of 1, 2, 3, 4, 5
    # Step 1: read the folder and load the problems (class Problem)
       # downloaded main folder put under main folder
    problem = load_problem_from_folder(main_dir, selected_question)
    # usage example
    print(#problem.problem_dir,
    #problem.problem_name,
    #problem.problem_description,
    #problem.sample_input,
    #problem.sample_output,
    #problem.full_input,
    #problem.full_output
    )

    return problem

# Step 2: solver



# Step 3: generate full_out.txt


if __name__=="__main__":
    if len(sys.argv) > 1:
        selected_question = int(sys.argv[1])
        problem = find_problem(selected_question)
        print(problem.problem_name)
    else:
        print("no problems found")

