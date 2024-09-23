import heapq

def solve_travelers_problem(N, K, S):
    # Create a min-heap for the crossing times
    heapq.heapify(S)  # Turn S into a min-heap

    # This list stores people who have already crossed
    crossed = []

    # Initialize total time to 0
    total_time = 0

    # While there are more than 3 people to cross
    while len(S) > 3:
        # Pop the two fastest and two slowest
        fastest1 = heapq.heappop(S)
        fastest2 = heapq.heappop(S)
        slowest1 = S[-1]  # Last (largest)
        slowest2 = S[-2]  # Second last (second largest)

        # Strategy 1: Fastest two cross, fastest returns, then slowest two cross, second fastest returns
        option1 = fastest1 + fastest1 + slowest1 + fastest2
        # Strategy 2: Fastest with slowest cross, fastest returns, repeat with next slowest
        option2 = fastest1 + fastest1 + fastest1 + fastest1

        if option1 < option2:
            total_time += option1
            # Slowest two cross, remove them from the heap
            S.pop()
            S.pop()
            heapq.heappush(S, fastest1)  # Fastest returns and remains in the heap
        else:
            total_time += option2
            # Slowest two cross, remove them from the heap
            S.pop()
            S.pop()
            heapq.heappush(S, fastest1)  # Fastest returns and remains in the heap

            # Push back the fastest person who returned to the other side
            heapq.heappush(S, fastest2)

    # Handle the last three or two people
    if len(S) == 3:
        total_time += S[2] + S[0] + S[1]
    elif len(S) == 2:
        total_time += S[1]
    elif len(S) == 1:
        total_time += S[0]

    # Return "YES" if the total time is within the limit K, otherwise "NO"
    return "YES" if total_time <= K else "NO"


# Main execution to read from stdin and output results
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    T = int(data[0])  # Number of test cases
    index = 1
    results = []
    
    for i in range(1, T + 1):
        N, K = map(int, data[index].split())
        S = list(map(int, data[index + 1:index + 1 + N]))
        index += N + 1
        result = solve_travelers_problem(N, K, S)
        results.append(f"Case #{i}: {result}")
    
    # Output all results at once
    sys.stdout.write("\n".join(results) + "\n")
