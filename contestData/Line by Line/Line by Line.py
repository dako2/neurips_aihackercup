def calculate_p_increase(n, p):
    """Calculates the increase in P needed to have the same success rate as typing one fewer line.

    Args:
        n: The original number of lines.
        p: The original probability of typing a line correctly.

    Returns:
        The increase in P needed.
    """

    p_new = (p / 100)**(n / (n - 1))  # Success probability with n-1 lines is same as success prob with n lines
    p_new_percentage = p_new * 100
    return p_new_percentage - p

t = int(input())

for i in range(1, t + 1):
    n, p = map(int, input().split())
    increase = calculate_p_increase(n, p)
    print(f"Case #{i}: {increase}")