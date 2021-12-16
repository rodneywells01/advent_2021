from collections import defaultdict

def parse_input():
    # Parse file input

    with open("input/15.txt") as f:

        lines = []
        for line in f.readlines():
            line = line.rstrip()
            line = [int(val) for val in line.rstrip()] 
            lines.append(line)
            
        return lines


class BFS_Search: 
    def __init__(self, maze):
        self.maze = maze
        self.goal = (len(maze[0])-1, len(maze)-1)


    def get_current_risk(self, position): 
        return self.maze[position[1]][position[0]]

    def search(self, current_position=(0,0), current_risk = 0):
        found_path = False 

        best_risk_to_positions = defaultdict(list) 
        position_risk_lookup = dict()  
        
        best_risk_to_positions[0] = [current_position]
        position_risk_lookup[current_position] = 0

        current_risk = -1
        best_path = None 

        while not (best_path and current_risk <= best_path): 
            # Let's get the minimum risk we can work with
            # TODO - Could get the min of the keys instead of this awkward increment
            positions = None
            while not positions:
                current_risk += 1 
                positions = best_risk_to_positions[current_risk]

            print(f"Looking at risk level {current_risk} | {len(positions)} positions")

            for position in positions: 
                neighbors = self.get_neighbors(position)
                for neighbor in neighbors: 
                    risk_to_position = current_risk + self.get_current_risk(neighbor)
                    best_risk_to_position = position_risk_lookup.get(neighbor) 
                    if not best_risk_to_position or risk_to_position < best_risk_to_position: 
                        position_risk_lookup[neighbor] = risk_to_position
                        best_risk_to_positions[risk_to_position].append(neighbor)

                        if neighbor == self.goal and (not best_path or best_path > risk_to_position):
                            best_path = risk_to_position

        return best_path

    def paint_path(self, path):
        pretty_map = [["." for val in row] for row in self.maze]

        for position in path: 
            pretty_map[position[1]][position[0]] = self.get_current_risk(position)


        for row in pretty_map: 
            row_str = " ".join([str(val) for val in row])
            print(row_str)

    def display_cave(self): 
        for row in self.maze: 
            row_str = " ".join([str(val) for val in row])
            print(row_str)

    def get_neighbors(self, position): 
        neighbors = []

        row_idx = position[0]
        col_idx = position[1]

        up_neighbor = row_idx - 1
        down_neighbor = row_idx + 1
        left_neighbor = col_idx - 1 
        right_neighbor = col_idx + 1

        if up_neighbor >= 0:
            neighbors.append((up_neighbor, col_idx))

        if down_neighbor < len(self.maze): 
            neighbors.append((down_neighbor, col_idx))

        if left_neighbor >= 0: 
            neighbors.append((row_idx,left_neighbor))

        if right_neighbor < len(self.maze[row_idx]):
            neighbors.append((row_idx,right_neighbor))

        return neighbors


def generate_full_cave_map(cave): 
    original_width = len(cave[0])
    original_height = len(cave)

    # for row in range(5):

    for row in range(5):
        for row_idx in range(original_height):
            for col in range(5): 
                if row == 0 and col == 0: 
                    continue 
                for col_idx in range(original_width):
                    original_value = cave[row_idx][col_idx]
                    new_value = original_value + (col + row)
                    while new_value > 9: 
                        new_value -= 9
                    
                    # Add the new value to the cave 
                    cave[row_idx + row * original_height].append(new_value) 

        # Starting a new segment, append original height 
        if row != 4:
            for _ in range(original_height):
                cave.append([])


    return cave


cave = parse_input()
cave = generate_full_cave_map(cave)
cave_searcher = BFS_Search(cave)
cave_searcher.display_cave()

min_risk = cave_searcher.search()
print(f"Final result: {min_risk}")
