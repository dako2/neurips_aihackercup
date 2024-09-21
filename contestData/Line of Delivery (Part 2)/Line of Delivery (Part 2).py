def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    
    results = []
    
    for tcase in range(1, t + 1):
        N = int(data[index])
        G = int(data[index + 1])
        index += 2
        
        energy = []
        for _ in range(N):
            energy.append(int(data[index]))
            index += 1
            
        positions = [0] * (N + 1)
        max_position = 0

        for i in range(N):
            Ei = energy[i]
            pos = positions[i] + Ei
            j = i + 1
            while j <= N and pos >= positions[j]:
                d = positions[j] - positions[i]
                remaining_energy = Ei - d
                positions[i] = positions[j] - 1
                Ei = remaining_energy
                i = j
                j += 1
                
            positions[i] = pos
            max_position = max(max_position, pos)
        
        closest_distance = float('inf')
        closest_index = -1
        
        for i in range(N):
            dist = abs(positions[i] - G)
            if dist < closest_distance:
                closest_distance = dist
                closest_index = i + 1  
                
        results.append(f"Case #{tcase}: {closest_index} {closest_distance}")
    
    for result in results:
        print(result)