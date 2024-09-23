import argparse
import random
from pathlib import Path
import re

def expand(total_cases, file_to_expand):
    with open(file_to_expand, 'r') as file:
        lines = file.readlines()

    if not lines:
        raise ValueError("The file is empty and cannot be expanded.")

    # Extract the case number pattern from the last line
    last_line = lines[-1].strip()
    match = re.match(r"(Case #(\d+))(.*)", last_line)
    
    if not match:
        raise ValueError("Last line does not contain a valid 'Case#' format.")

    last_case_number = int(match.group(2))
    remaining_lines_needed = total_cases - len(lines)

    # If no expansion is needed
    if remaining_lines_needed <= 0:
        print(f"The file already contains {len(lines)} lines, which is greater than or equal to {total_cases}.")
        return

    # Create the expanded lines by incrementing the Case# and appending the rest of the line
    with open(file_to_expand, 'a') as file:
        for i in range(1, remaining_lines_needed + 1):
            new_case_number = last_case_number + i
            new_line = f"Case #{new_case_number}{match.group(3)}\n"
            file.write(new_line)

    print(f"File expanded to {total_cases} lines by duplicating the last line with incremented Case#.")

#expand(95, 'contestData/Walk the Line/sample_out copy.txt')
expand(85, 'contestData/Line of Delivery (Part 2)/sample_out copy.txt')