def get_slope(x1, y1, x2, y2):
    if x1 == x2:
        return float('inf')
    return (y2 - y1) / (x2 - x1)

def count_moves(N, points):
    if N <= 2:
        return 0
    
    slope = get_slope(points[0][0], points[0][1], points[1][0], points[1][1])
    moves = 0
    for i in range(2, N):
        current_slope = get_slope(points[0][0], points[0][1], points[i][0], points[i][1])
        if current_slope != slope:
            moves += 1
    return moves

T = int(input())
for i in range(1, T+1):
    N = int(input())
    points = []
    for _ in range(N):
        x, y = map(int, input().split())
        points.append((x, y))
    moves = count_moves(N, points)
    print(f"Case #{i}: {moves}")