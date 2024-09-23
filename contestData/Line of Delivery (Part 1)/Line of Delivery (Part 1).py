def solve_curling(N, G, energies):
    """
    Solves the curling problem for a single test case.

    Args:
        N: The number of stones.
        G: The goal position.
        energies: A list of energies for each stone.

    Returns:
        A tuple containing the index of the closest stone to the goal and its distance.
    """
    # Sort stones by energy to simulate collisions in order of energy
    sorted_energies = sorted(enumerate(energies), key=lambda x: x[1], reverse=True)
    # Initialize the positions of all stones to 0
    positions = [0] * N
    # Keep track of the closest stone and its distance
    closest_stone = 0
    min_distance = G  # Initialize to the maximum possible distance
    
    # Simulate the movement of the stones
    for i, (stone_index, energy) in enumerate(sorted_energies):
        current_position = positions[stone_index]
        while energy > 0:
            # Move the stone one unit if possible
            if current_position + 1 <= G:
                current_position += 1
                energy -= 1
            # Collision with a stationary stone, transfer energy
            else:
                break
        # Update the position of the stone
        positions[stone_index] = current_position
        # Update the closest stone if necessary
        distance = abs(current_position - G)
        if distance < min_distance:
            min_distance = distance
            closest_stone = stone_index
        elif distance == min_distance and stone_index < closest_stone:
            closest_stone = stone_index

    return closest_stone + 1, min_distance

# Read input from the user
T = int(input())

# Solve each test case
for i in range(1, T + 1):
    N, G = map(int, input().split())
    energies = []
    for _ in range(N):
        energies.append(int(input()))
    # Solve the case
    closest_stone, distance = solve_curling(N, G, energies)
    # Print the output
    print(f"Case #{i}: {closest_stone} {distance}")