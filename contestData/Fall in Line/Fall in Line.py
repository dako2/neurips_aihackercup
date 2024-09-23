from tqdm import tqdm
def calculate_distance(x1, y1, x2, y2):
  """Calculates the distance between two points."""
  return abs(x1 - x2) + abs(y1 - y2)

def count_ants_on_line(x_coords, y_coords, slope, intercept):
  """Counts the number of ants that lie on a given line."""
  count = 0
  for i in range(len(x_coords)):
    if abs(y_coords[i] - (slope * x_coords[i] + intercept)) <= 1e-6:  # Allow for small floating-point errors
      count += 1
  return count

def solve_ant_line(x_coords, y_coords):
  """Finds the maximum number of ants that can lie on a single line."""
  max_ants_on_line = 2  # Start with at least two ants on a line
  for i in tqdm(range(len(x_coords))):
    for j in range(i + 1, len(x_coords)):
      # Calculate the slope and intercept of the line passing through two ants
      if x_coords[i] == x_coords[j]:
        slope = float('inf')
        intercept = 0  # Arbitrary value, as the line is vertical
      else:
        slope = (y_coords[i] - y_coords[j]) / (x_coords[i] - x_coords[j])
        intercept = y_coords[i] - slope * x_coords[i]

      # Count ants on this line
      current_ants_on_line = count_ants_on_line(x_coords, y_coords, slope, intercept)
      max_ants_on_line = max(max_ants_on_line, current_ants_on_line)

  return len(x_coords) - max_ants_on_line  # Ants to move = total ants - max on a line

if __name__ == "__main__":
  T = int(input())
  for t in range(1, T + 1):
    N = int(input())
    x_coords = []
    y_coords = []
    for _ in range(N):
      X, Y = map(int, input().split())
      x_coords.append(X)
      y_coords.append(Y)
    
    result = solve_ant_line(x_coords, y_coords)
    print(f"Case #{t}: {result}")