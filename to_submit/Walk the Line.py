def solve(N, K, S):
    S.sort()
    time = 0
    crossed = 0
    while crossed < N:
        if crossed == N - 1:
            time += S[crossed]
            crossed += 1
        elif crossed == N - 2:
            time += S[crossed]
            crossed += 2
        else:
            time += S[crossed + 1]
            time += S[crossed]
            crossed += 2
    return time <= K


T = int(input())
for i in range(1, T + 1):
    N, K = map(int, input().split())
    S = [int(input()) for _ in range(N)]

    if solve(N, K, S):
        print(f"Case #{i}: YES")
    else:
        print(f"Case #{i}: NO")