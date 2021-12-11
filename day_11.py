def parse_input():
    # Parse file input
    lines = []
    with open("input/11.txt") as f:
        raw_lines = [line.rstrip() for line in f.readlines()]
        for row_idx in range(len(raw_lines)):
            row = []
            for octopus in raw_lines[row_idx]: 
                row.append(int(octopus))
            lines.append(row)

    return lines 

octopuses = parse_input()
print(octopuses)

def get_neighbors_idx(row_idx, col_idx, values=True): 
    neighbors = set()

    up_neighbor = row_idx - 1
    down_neighbor = row_idx + 1
    left_neighbor = col_idx - 1 
    right_neighbor = col_idx + 1


    if up_neighbor >= 0:
        neighbors.add((up_neighbor,col_idx))

        if left_neighbor >= 0: 
            neighbors.add((up_neighbor,left_neighbor))
        if right_neighbor < len(octopuses[row_idx]):
            neighbors.add((up_neighbor,right_neighbor))

    if down_neighbor < len(octopuses): 
        neighbors.add((down_neighbor,col_idx))

        if left_neighbor >= 0: 
            neighbors.add((down_neighbor,left_neighbor))
        if right_neighbor < len(octopuses[row_idx]):
            neighbors.add((down_neighbor,right_neighbor))

    if left_neighbor >= 0: 
        neighbors.add((row_idx,left_neighbor))

    if right_neighbor < len(octopuses[row_idx]):
        neighbors.add((row_idx,right_neighbor))


    return neighbors   


flash_count = 0 

def step(): 
    # Find all 9s and flash. Repeat until there are no nines. 
    flash_octopuses = set()
    flashed_octopuses = set()

    # Increment all by one and collect all nines. 
    for row_idx in range(len(octopuses)):
        for col_idx in range(len(octopuses[row_idx])):
            octopuses[row_idx][col_idx] += 1
            if octopuses[row_idx][col_idx] == 10: 
                flash_octopuses.add((row_idx, col_idx))


    # print("Hello")
    # print(flash_octopuses)
    # print(flashed_octopuses)

    while len(flash_octopuses) > 0:
        octopus = flash_octopuses.pop()
        neighbors = get_neighbors_idx(octopus[0], octopus[1])

        for neighbor in neighbors: 
            row_idx = neighbor[0]
            col_idx = neighbor[1]
            # print(neighbor)
            
            if octopuses[row_idx][col_idx] <= 9:
                octopuses[row_idx][col_idx] += 1
            # else: 
            #     print("This is already 10")

            if octopuses[row_idx][col_idx] > 9 and neighbor not in flash_octopuses and neighbor not in flashed_octopuses:
                print("Adding!")
                flash_octopuses.add(neighbor)


        # print(octopuses)
        flashed_octopuses.add(octopus)

    # Now reset all flashed octopuses 
    flash_count = len(flashed_octopuses)

    if flash_count == len(octopuses) * len(octopuses[0]): 
        return True 

    for octopus in flashed_octopuses: 
        octopuses[octopus[0]][octopus[1]] = 0

    return False

def pretty_print(stuff): 
    for row in stuff:
        print(row)

# for _ in range(100):
#     pretty_print(octopuses)
#     print("Starting step")
#     flash_count += step()
#     pretty_print(octopuses)
#     print(flash_count)


finished = False 
count = 0 
while not finished:
    finished = step() 
    count += 1

print("Done!")
print(count)