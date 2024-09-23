def solve(N, K, times):
    """
    Solves the bridge crossing problem.

    Args:
        N: The number of travelers.
        K: The time limit.
        times: A list of crossing times for each traveler.

    Returns:
        "YES" if all travelers can cross within the time limit, "NO" otherwise.
    """

    # Sort travelers by crossing time in ascending order.
    times.sort()

    # Initialize the total time and the number of travelers crossed.
    total_time = 0
    crossed = 0

    # Simulate the bridge crossing.
    while crossed < N:
        # If only one traveler is left, they cross alone.
        if crossed == N - 1:
            total_time += times[crossed]
            crossed += 1
            continue

        # If two travelers can cross together, choose the fastest two.
        if total_time + times[crossed] + times[crossed + 1] <= K:
            total_time += times[crossed + 1]  # Fastest crosses with wheelbarrow
            crossed += 2
        else:
            # If two cannot cross together, the fastest crosses alone and returns.
            total_time += times[crossed]
            total_time += times[crossed]
            crossed += 1

    # Check if all travelers crossed within the time limit.
    if total_time <= K:
        return "YES"
    else:
        return "NO"


if __name__ == "__main__":
    T = int(input())
    for i in range(1, T + 1):
        N, K = map(int, input().split())
        times = []
        for _ in range(N):
            times.append(int(input()))

        result = solve(N, K, times)
        print(f"Case #{i}: {result}")