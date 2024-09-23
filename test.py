from score import save_best_scores, load_best_scores
from utils import load_problem_from_folder
import pathlib

main_dir = pathlib.Path("./contestData")   # downloaded main folder put under main folder
problem = load_problem_from_folder(main_dir, 5)

print(load_best_scores(problem))