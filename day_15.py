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
        # self.safest_route = None 
        self.start = (0,0)
        # print(maze)
        self.goal = (len(maze[0])-1, len(maze)-1)


        # Direct route 
        self.safest_route = None 

        self.best_risk_at_position = dict()
        self.best_path = None


    def get_current_risk(self, position): 
        return self.maze[position[1]][position[0]]

    def dive_to_goal(self, position): 
        # We need to attempt to dive to the goal to improve our best_risk. 


        path = self.maze[position[1]][position[0]:] + [row[len(self.maze[0]) - 1] for row in self.maze[position[1] + 1:]]
        vert_path = [row[position[0]] for row in self.maze[position[1]:]] + self.maze[len(self.maze)-1][position[0]:]

        # Risk is already included in this position
        best_path = min(sum(path), sum(vert_path))

        best_path -= self.maze[position[1]][position[0]]
        return best_path

    def search(self, path=None, current_position=(0,0), current_risk = 0, layer =0):
        print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")
        # print(path)


        # Evaluate if we're making progress here or not. 
        best_performance = self.best_risk_at_position.get(current_position) 
        if not best_performance or best_performance > current_risk:
            self.best_risk_at_position[current_position] = current_risk
            # if path:
            #     new_best_path = path.copy() 
            #     new_best_path.add(current_position)
            #     self.best_path = new_best_path
        else: 
            # There is no point in continuing to explore this path. 
            # print(f"{current_risk} does not beat {self.best_risk_at_position[current_position]}")
            return 

        if not path: 
            path = set()

        if current_position == self.goal:
            if current_risk < self.safest_route:
                self.safest_route = min(self.safest_route, current_risk)
                print(f"New safest route! Risk: {current_risk}")
                self.paint_path(path)
                self.best_path = path
            print(f"Safest is {self.safest_route}")
            return 

        # if layer > 250: 
        dive_risk = self.dive_to_goal(current_position) + current_risk
        print(dive_risk)
        self.safest_route = min(self.safest_route, self.dive_to_goal(current_position) + current_risk)

        if current_risk >= self.safest_route:
            # print(f"{current_risk} is too unsafe!")
            return

        # Get your neighbors and add them to the search. 
        neighbors = self.get_neighbors(current_position) 

        neighbors = set(neighbors) - path

        if not neighbors: 
            # print("Out of valid neighbors!")
            return
        # print(neighbors)

        # Sort the neighbors based on their low cost. 
        sorted_neighbors = [] 
        lookup = defaultdict(list) 

        for neighbor in neighbors:
            risk = self.get_current_risk(neighbor)
            lookup[risk].append(neighbor)

        for key in sorted(list(lookup.keys())):
            sorted_neighbors += lookup[key]

        # risks = []
        # for neighbor in sorted_neighbors:
        #     risks.append(self.get_current_risk(neighbor))

        # print(risks)

        
        # TODO - Prioritize by risk level 
        for neighbor in sorted_neighbors: 
            # print(f"Neighbor: {neighbor} | Path: {path}")
            if neighbor not in path: 
                # print(f"Neighbor: {neighbor} | Path: {path}")
                new_path = path.copy()
                new_path.add(neighbor)

                # print(f"After adding: Neighbor: {neighbor} | Path: {path}")
                self.search(
                    new_path, 
                    neighbor, 
                    current_risk + self.maze[neighbor[1]][neighbor[0]],
                    layer=layer+1
                )


        # We need to search. Find the neighbors and travel if we have not been there. 


        if not path: 
            print("Done!")
            # print(safest_route)
            return self.safest_route

        return

    def better_search(self, current_position=(0,0), current_risk = 0, layer =0):
        # print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")

        # Evaluate if we're making progress here or not. 
        best_performance = self.best_risk_at_position.get(current_position) 
        if not best_performance or best_performance >= current_risk:
            self.best_risk_at_position[current_position] = current_risk
        else: 
            # There is no point in continuing to explore this path. 
            print(f"{best_performance} is worse than {current_risk}")
            return 

        if current_position == self.goal:
            if current_risk < self.safest_route:
                print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")

                self.safest_route = min(self.safest_route, current_risk)
                # print(f"New safest route! Risk: {current_risk}")
                # self.paint_path(path)
                # self.best_path = path
            print(f"Safest is {self.safest_route}")
            return 

        # if layer > 250: 
        dive_risk = self.dive_to_goal(current_position) + current_risk
        if self.safest_route > self.dive_to_goal(current_position) + current_risk:
            self.safest_route = self.dive_to_goal(current_position) + current_risk
            print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")

        if current_risk > self.safest_route:
            return

        # Get your neighbors and add them to the search. 
        neighbors = self.get_neighbors(current_position) 

        
        # TODO - Prioritize by risk level 
        for neighbor in neighbors: 
            # print(f"Neighbor: {neighbor} | Path: {path}")
            best_cost = self.best_risk_at_position.get(neighbor)
            cost_to_move = current_risk + self.get_current_risk(neighbor)

            if not best_cost or best_cost > cost_to_move: 
                self.best_risk_at_position[neighbor] = cost_to_move
    
                # print(f"After adding: Neighbor: {neighbor} | Path: {path}")
                self.better_search(
                    neighbor, 
                    cost_to_move,
                    layer=layer+1
                )


        # We need to search. Find the neighbors and travel if we have not been there. 
        if layer == 0:
            print("We're done!")
            return self.safest_route
        return

    def best_search(self, current_position=(0,0), current_risk = 0):
        # print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")

        found_path = False 

        best_risk_to_positions = defaultdict(list) 
        position_risk_lookup = dict()  
        
        best_risk_to_positions[0] = [current_position]
        position_risk_lookup[current_position] = 0


        current_risk = -1
        best_path = None 

        while not found_path: 
            # Let's get the minimum risk we can work with
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


            if best_path and best_path <= current_risk: 
                # We're done. 
                break 

        return best_path





        # Evaluate if we're making progress here or not. 
        best_performance = self.best_risk_at_position.get(current_position) 
        if not best_performance or best_performance >= current_risk:
            self.best_risk_at_position[current_position] = current_risk
        else: 
            # There is no point in continuing to explore this path. 
            print(f"{best_performance} is worse than {current_risk}")
            return 

        if current_position == self.goal:
            if current_risk < self.safest_route:
                print(f"Exploring layer {layer} | {current_risk} | {self.safest_route}")

                self.safest_route = min(self.safest_route, current_risk)
                # print(f"New safest route! Risk: {current_risk}")
                # self.paint_path(path)
                # self.best_path = path
            print(f"Safest is {self.safest_route}")
            return 

        
        if current_risk > self.safest_route:
            return

        # Get your neighbors and add them to the search. 
        neighbors = self.get_neighbors(current_position) 

        
        # TODO - Prioritize by risk level 
        for neighbor in neighbors: 
            # print(f"Neighbor: {neighbor} | Path: {path}")
            best_cost = self.best_risk_at_position.get(neighbor)
            cost_to_move = current_risk + self.get_current_risk(neighbor)

            if not best_cost or best_cost > cost_to_move: 
                self.best_risk_at_position[neighbor] = cost_to_move
    
                # print(f"After adding: Neighbor: {neighbor} | Path: {path}")
                self.better_search(
                    neighbor, 
                    cost_to_move,
                    layer=layer+1
                )


        # We need to search. Find the neighbors and travel if we have not been there. 
        if layer == 0:
            print("We're done!")
            return self.safest_route
        return


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




cave = parse_input()


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


cave = generate_full_cave_map(cave)
cave_searcher = BFS_Search(cave)
cave_searcher.display_cave()

path = cave_searcher.best_search()
print("Final result:")
print(path)

# print(cave_searcher.best_path)
# cave_searcher.paint_path(cave_searcher.best_path)


# neighbors = set(cave_searcher.get_neighbors((1,2))) 
# cave_searcher.paint_path(neighbors)
# print("Nice!")
# print(neighbors)