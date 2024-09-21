def calculate_increase(N, P):
  """Calculates the increase in P needed to have the same chance of success as typing one fewer line.

  Args:
    N: Number of lines in the original solution.
    P: Original success probability (percentage).

  Returns:
    The increase in P needed for equal success probability.
  """
  # Calculate the probability of success for N-1 lines with original P
  success_prob_n_minus_1 = (P / 100) ** (N - 1)

  # Calculate the required P for N lines to have the same success probability
  required_p = (success_prob_n_minus_1) ** (1 / N) * 100

  # Calculate the increase in P
  increase = required_p - P

  return increase

# Read the number of test cases
T = int(input())

# Process each test case
for i in range(1, T + 1):
  N, P = map(int, input().split())

  # Calculate the increase in P and print the result
  increase = calculate_increase(N, P)
  print(f"Case #{i}: {increase}")