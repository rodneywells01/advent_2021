def parse_input():
    # Parse file input
    cave_nodes = dict() 
    
    with open("input/12.txt") as f:
        # Each line contains 2 caves 
        for line in f.readlines():
            line = line.rstrip()
            cave_names = line.split("-")

            for cave in cave_names: 
                if cave not in cave_nodes.keys(): 
                    # Create a new cave node. 
                    cave_nodes[cave] = GraphNode(cave)

            # Add the relationship between the two caves 
            cave_nodes[cave_names[0]].add_neighbor(cave_names[1])
            cave_nodes[cave_names[1]].add_neighbor(cave_names[0])


        
    return cave_nodes


class GraphNode: 
    def __init__(self, name, neighbors=None): 
        self.name = name 
        self.is_big = self.name.isupper()

        if not neighbors:
            self.neighbors = []
        else:
            self.neighbors = neighbors

    def add_neighbor(self, neighbor): 
        self.neighbors.append(neighbor)

    def __str__(self): 
        return f"Cave: '{self.name}' | Neighbors: '{', '.join(self.neighbors)}'"



valid_paths = set()
def find_paths_part_one(node_name, path):
    if path == "": 
        path = node_name
    else:
        path += f",{node_name}"

    if node_name == "end": 
        valid_paths.add(path)

    else:
        visited_nodes = set(path.split(","))    

        # Let's go exploring!!!
        for neighbor in cave_nodes[node_name].neighbors:
            if cave_nodes[neighbor].is_big or neighbor not in visited_nodes:
                find_paths_part_one(neighbor, path) 


def find_paths_part_two(node_name, path, extra_visit=False):
    if path == "": 
        path = node_name
    else:
        path += f",{node_name}"

    if node_name == "end": 
        valid_paths.add(path)

    else:
        visited_nodes = set(path.split(","))    

        # Let's go exploring!!!
        for neighbor in cave_nodes[node_name].neighbors:
            if cave_nodes[neighbor].is_big:
                find_paths_part_two(neighbor, path, extra_visit=extra_visit) 
            else: 
                if neighbor not in visited_nodes:  
                    find_paths_part_two(neighbor, path, extra_visit=extra_visit) 
                elif neighbor in visited_nodes and not extra_visit and neighbor not in set(["start", "end"]): 
                    find_paths_part_two(neighbor, path, extra_visit=True) 


cave_nodes = parse_input()

find_paths_part_one("start", "")
print(f"Part One: {len(valid_paths)}")

valid_paths = set()
find_paths_part_two("start", "")
print(f"Part Two: {len(valid_paths)}")
