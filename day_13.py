def parse_input():
    # Parse file input
    dot_positions = list()
    fold_instructions = list()
    reading_fold_instructions = False 

    with open("input/13.txt") as f:
        for line in f.readlines():
            line = line.rstrip()

            if not reading_fold_instructions:
                if line == "": 
                    reading_fold_instructions = True 
                else:
                    dot_positions.append([int(val) for val in line.split(",")])
            else: 
                fold_instructions.append(line.split()[2])
        
    return dot_positions, fold_instructions


# Build the paper 
def fold(paper, fold_instruction): 
    instruction_pieces = fold_instruction.split("=")
    fold_plane = instruction_pieces[0]
    fold_line = int(instruction_pieces[1])

    # Find the smaller, apply the smaller to the larger. 
    folded_pieces = []
    if fold_plane == "y": 
        folded_pieces.append(paper[:fold_line])
        folded_pieces.append(paper[fold_line + 1:])
    elif fold_plane == "x":
        folded_pieces.append([row[:fold_line] for row in paper])
        folded_pieces.append([row[fold_line + 1:] for row in paper])
    else: 
        raise Exception(f"We can't handle fold_plane {fold_plane}")


    # Now apply the fold 
    # TODO: Handle folds of unequal size 
    folded_paper = folded_pieces[0]
    for row_idx in range(len(folded_pieces[1])):
        for col_idx, value in enumerate(folded_pieces[1][row_idx]):
            # Set the value on the other half 
            if value is "#":
                # Determine the correct row and col idxs on the folded page
                folded_row_idx = row_idx
                folded_col_idx = col_idx
                if fold_plane == "y": 
                    folded_row_idx = len(folded_pieces[1]) - 1 - row_idx
                else: 
                    folded_col_idx = len(folded_pieces[1][row_idx]) - 1 - col_idx

                # Update the value on the folded sheet. 
                folded_paper[folded_row_idx][folded_col_idx] = value

    print(f"Here is the fold on {fold_plane}={str(fold_line)}")
    pretty_print(folded_paper)
    print()

    return folded_paper

def generate_paper(dot_positions): 
    # Determine dimensions of the paper. 
    max_x = 0
    max_y = 0 
    for dot in dot_positions: 
        if dot[1] + 1 > max_y:
            max_y = dot[1] + 1 
        if dot[0] + 1 > max_x:
            max_x = dot[0] + 1 

    # Build the paper 
    paper = [["." for _ in range(max_x)] for _ in range(max_y)]
    for dot in dot_positions: 
        paper[dot[1]][dot[0]] = "#"

    return paper 

def pretty_print(paper): 
    for row in paper: 
        pretty_row = " ".join([val for val in row])
        print(pretty_row)

def solve_problem(dot_positions, fold_instructions): 
    paper = generate_paper(dot_positions)
    for fold_instruction in fold_instructions: 
        paper = fold(paper, fold_instruction)

    dot_count = count_dots(paper)

    return dot_count 


def count_dots(paper): 
    dot_count = 0 
    for row in paper: 
        for value in row: 
            if value == "#": 
                dot_count += 1

    return dot_count

def main():
    dot_positions, fold_instructions = parse_input()
    final_result = solve_problem(dot_positions, fold_instructions)
    print(final_result)


if __name__ == "__main__":
    main()