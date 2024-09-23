import json
import logging
from pathlib import Path

def save_best_scores(problem, filepath='best_scores.json'):
    data = {
        'best_score': problem.best_score,
        'best_code_path': str(problem.best_code_path),
        'best_full_out_path': str(problem.best_full_out_path)
    }
    with open(str(problem.problem_dir) + '/'+ filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_best_scores(problem, filepath='best_scores.json'):
    try:
        with open(str(problem.problem_dir) + '/'+ filepath, 'r') as f:
            data = json.load(f)
        return data.get('best_score', 0)
    except FileNotFoundError:
        logging.info("No existing best scores found. Starting fresh.")
    except Exception as e:
        logging.error(f"Failed to load best scores: {e}", exc_info=True)