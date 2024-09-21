def solve(N, K, times):
    """
    Solves the bridge crossing problem.

    Args:
        N: The number of travelers.
        K: The time limit.
        times: A list of crossing times for each traveler.

    Returns:
        "YES" if the travelers can cross within K seconds, "NO" otherwise.
    """

    # Sort the travelers by their crossing times in ascending order.
    times.sort()

    # If there's only one traveler, they can cross in their own time.
    if N == 1:
        return "YES" if times[0] <= K else "NO"

    # Calculate the time required for the fastest two to cross, then return
    # the flashlight.
    fastest_crossing_time = times[0] + times[1]

    # If the two fastest can't cross within the time limit, it's impossible.
    if fastest_crossing_time > K:
        return "NO"

    # The fastest two cross, then the fastest returns.
    remaining_time = K - fastest_crossing_time - times[0]

    # Now, the two slowest travelers can cross, and the second-fastest
    # returns.
    if times[-1] + times[-2] <= remaining_time:
        return "YES"

    # Otherwise, it's impossible.
    return "NO"


T = int(input())
for i in range(1, T + 1):
    N, K = map(int, input().split())
    times = []
    for _ in range(N):
        times.append(int(input()))
    print(f"Case #{i}: {solve(N, K, times)}")