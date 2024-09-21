3
import math

def calculate_increase(n, p):
    return math.sqrt(p / 100) * math.sqrt(100 - p) * (n - 1) / n

T = int(input())

for i in range(1, T + 1):
    N, P = map(int, input().split())
    increase = calculate_increase(N, P)
    print(f"Case #{i}: {increase}")