def solve_travelers_problem():
    T = int(input())  # Number of test cases
    
    for case_num in range(1, T + 1):
        N, K = map(int, input().split())  # Read N and K
        S = [int(input()) for _ in range(N)]  # Read the crossing times
        
        # If there's only one traveler
        if N == 1:
            if S[0] <= K:
                print(f"Case #{case_num}: YES")
            else:
                print(f"Case #{case_num}: NO")
            continue
        
        # Sort the crossing times in ascending order
        S.sort()
        
        # Initialize total time to 0
        total_time = 0
        left = N  # Number of people left to cross
        
        while left > 3:
            # Strategy 1: Send the two fastest across, fastest returns, then send two slowest across, second fastest returns
            option1 = S[1] + S[0] + S[left - 1] + S[1]
            # Strategy 2: Send the fastest with the slowest across, fastest returns, repeat
            option2 = S[left - 1] + S[0] + S[left - 2] + S[0]
            total_time += min(option1, option2)
            
            # Two people have crossed, reduce the number of people left
            left -= 2
        
        # For the last 3 or fewer people
        if left == 3:
            total_time += S[2] + S[0] + S[1]
        elif left == 2:
            total_time += S[1]
        
        # Output the result for this test case
        if total_time <= K:
            print(f"Case #{case_num}: YES")
        else:
            print
            
solve_travelers_problem()