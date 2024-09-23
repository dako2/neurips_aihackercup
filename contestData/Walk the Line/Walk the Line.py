def solve(N, K, S):
    S.sort()
    time = 0
    i = 0
    while i < N:
        if i == N - 1:
            time += S[i]
            i += 1
        else:
            time += S[i + 1]
            time += max(S[i], S[i + 1])
            i += 2
    return time <= K


if __name__ == '__main__':
    T = int(input())

    for i in range(1, T + 1):
        N, K = map(int, input().split())
        S = []
        for _ in range(N):
            S.append(int(input()))

        if solve(N, K, S):
            print(f"Case #{i}: YES")
        else:
            print(f"Case #{i}: NO")