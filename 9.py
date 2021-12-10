def parse_input():
    # Parse file input

    output_values = []
    signal_patterns = []

    with open("input/9.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]

        print(lines)

    return lines 



heightmap = parse_input()


def djikstras(current, basin=None):
    if not basin:
        basin = set()
    row, col = current.split(",")
    row = int(row)
    col = int(col)
    neighbors = get_neighbors_2(row, col)

    queue = []

    for neighbor in neighbors: 
        row, col = neighbor.split(",")
        row = int(row)
        col = int(col)
        val = int(heightmap[row][col])

        if val != 9: 
            # print(basin)
            if neighbor not in basin:
                print(f"Adding {neighbor}")
                basin.add(neighbor)
                queue.append(neighbor)

    for neighbor in queue: 
        basin = djikstras(neighbor, basin)


    return basin


def get_neighbors_2(row_idx, col_idx): 
    neighbors = []

    up_neighbor = row_idx - 1
    down_neighbor = row_idx + 1
    left_neighbor = col_idx - 1 
    right_neighbor = col_idx + 1


    if up_neighbor >= 0:
        neighbors.append(f"{up_neighbor},{col_idx}")

    if down_neighbor < len(heightmap): 
        neighbors.append(f"{down_neighbor},{col_idx}")

    if left_neighbor >= 0: 
        neighbors.append(f"{row_idx},{left_neighbor}")

    if right_neighbor < len(heightmap[row_idx]):
        neighbors.append(f"{row_idx},{right_neighbor}")

    return neighbors    

def get_neighbors(row_idx, col_idx): 
    neighbors = []

    up_neighbor = row_idx - 1
    down_neighbor = row_idx + 1
    left_neighbor = col_idx - 1 
    right_neighbor = col_idx + 1


    if up_neighbor >= 0:
        neighbors.append(heightmap[up_neighbor][col_idx])

    if down_neighbor < len(heightmap): 
        neighbors.append(heightmap[down_neighbor][col_idx])

    if left_neighbor >= 0: 
        neighbors.append(heightmap[row_idx][left_neighbor])

    if right_neighbor < len(heightmap[row_idx]):
        neighbors.append(heightmap[row_idx][right_neighbor])

    return neighbors

score = 0 
basin_sizes = []

for row_idx in range(len(heightmap)):
    for col_idx in range(len(heightmap[row_idx])):
        current = int(heightmap[row_idx][col_idx])
        neighbors = get_neighbors(row_idx, col_idx)
        if all([current < int(neighbor) for neighbor in neighbors]): 
            # Explore the basin. 
            # score += current + 1

            print(f"Discovering basin for {row_idx},{col_idx}")
            basin = djikstras(f"{row_idx},{col_idx}")

            # Save the basin size
            basin_sizes.append(len(basin))


# Determine the 3 largest basins 
basin_sizes.sort(reverse=True)
final_result = 1 
print(basin_sizes)
for size in basin_sizes[:3]:
    final_result *= size


print(final_result)