def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    T = int(data[index])
    index += 1
    results = []
    
    from sortedcontainers import SortedDict
    
    for case_number in range(1, T + 1):
        N = int(data[index])
        G = int(data[index + 1])
        index += 2
        energies = []
        
        for i in range(N):
            E = int(data[index])
            energies.append((E, i + 1))  # We shuttle energy and original index
            index += 1

        # Sort energies by the amount of energy (ascending)
        energies.sort()
        
        final_positions = SortedDict()
        final_info = [None] * (N + 1)  # Store (position, index) for easier result fetching
        
        for energy, stone_index in energies:
            position = energy
            
            # Simulation of collision and carry
            while position in final_positions:
                carried_energy = position - final_positions[position] + 1
                final_positions.pop(position)  # This stone will move further
                position += carried_energy
            
            final_positions[position] = position  # Now this stone settles here
            final_info[stone_index] = (position, stone_index)
        
        # Find the stone that is closest to G
        closest_distance = float('inf')
        closest_stone_index = None
        
        for stone_index in range(1, N + 1):
            position, idx = final_info[stone_index]
            distance = abs(position - G)
            if distance < closest_distance or (distance == closest_distance and stone_index < closest_stone_index):
                closest_distance = distance
                closest_stone_index = stone_index
        
        results.append(f"Case #{case_number}: {closest_stone_index} {closest_distance}")

    # Print all results at once to respect the Large I/O operations
    sys.stdout.write("\n".join(results) + "\n")