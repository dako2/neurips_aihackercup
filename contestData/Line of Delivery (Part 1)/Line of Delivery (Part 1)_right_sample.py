def solve(n, g, energies):
  """
  Solves the curling game for a single test case.

  Args:
    n: Number of stones.
    g: Goal position.
    energies: List of energies for each stone.

  Returns:
    A tuple containing the index of the closest stone and its distance from the goal.
  """

  # Sort the energies in descending order to simulate collision order
  energies.sort(reverse=True)

  # Initialize a list to store the final positions of the stones
  positions = [0] * n

  # Simulate the game
  current_energy = 0
  current_position = 0
  for i, energy in enumerate(energies):
    # If there's remaining energy from the previous stone, transfer it
    if current_energy:
      positions[i] = current_position
      current_energy -= 1
      current_position += 1
      continue

    # Move the current stone
    current_energy = energy
    current_position = 0
    while current_energy > 0:
      current_position += 1
      current_energy -= 1

    # Store the final position of the stone
    positions[i] = current_position

  # Find the closest stone to the goal
  closest_stone_index = 0
  closest_distance = abs(positions[0] - g)
  for i, position in enumerate(positions):
    distance = abs(position - g)
    if distance < closest_distance:
      closest_distance = distance
      closest_stone_index = i
    elif distance == closest_distance and i < closest_stone_index:
      closest_stone_index = i

  return closest_stone_index + 1, closest_distance

# Read input
t = int(input())
for i in range(1, t + 1):
  n, g = map(int, input().split())
  energies = [int(input()) for _ in range(n)]

  # Solve the problem
  closest_stone_index, closest_distance = solve(n, g, energies)

  # Print the output
  print(f"Case #{i}: {closest_stone_index} {closest_distance}")