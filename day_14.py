from collections import defaultdict


def parse_input():
    # Parse file input

    with open("input/14.txt") as f:
        polymer_substitution = dict() 

        first_line = True 
        print("Hello?")
        for line in f.readlines():
            line = line.rstrip()

            if not line:
                continue

            if first_line: 
                polymer_template = line 
                first_line = False
            else:
                line_pieces = line.split()

                polymer_input = line_pieces[0]
                polymer_insertion = line_pieces[2]

                # print(f"{polymer_input} => {polymer_insertion} ")
                polymer_substitution[polymer_input] = polymer_insertion
        
    return polymer_template, polymer_substitution


polymer_template, polymer_substitution = parse_input() 

def solve_problem(elem_count): 
    # Find the largest and the smallest. 
    most_common = None
    least_common = None
    

    for elem, count in elem_count.items(): 
        print(f"{elem} occurs {count} times")
        if not most_common or count > elem_count[most_common]:
            most_common = elem
        if not least_common or count < elem_count[least_common]:
            least_common = elem 

    print(f"{most_common}, {least_common}") 

    print(elem_count)


    return elem_count[most_common] - elem_count[least_common]

def build_polymer(iterations, polymer, polymer_substitution): 
    substitution_locations = dict() 


    for iteration in range(iterations): 
        new_polymer = "" 
        idx = 0 
        while idx < len(polymer):
            # print(len(polymer))
            # print(idx)
            two_value_polymer = polymer[idx:min(idx+2, len(polymer))]
            # print(two_value_polymer)

            new_polymer += polymer[idx]

            if two_value_polymer in polymer_substitution: 
                # print(f"inserting into {two_value_polymer} value {polymer_substitution[two_value_polymer]}" )
                new_polymer += polymer_substitution[two_value_polymer]
            
            idx += 1
            # print(new_polymer)
        # new_polymer += polymer[idx]
        # print(new_polymer)
        polymer = new_polymer

        print(f"{iteration} | {iteration / iterations * 100}%")

        # assert step_validation[iteration + 1] == polymer, f"{iteration + 1} | {step_validation[iteration + 1]} != {polymer}"


    return polymer


def build_polymer_better(iterations, polymer, polymer_substitution): 
    polymer_occurences = defaultdict(int)
    element_occurences = defaultdict(int)
    # Build the pairs into the polymer occurences 
    for idx in range(len(polymer) - 1):
        elem = polymer[idx: idx + 2]
        polymer_occurences[elem] += 1 

        if idx == 0:
            element_occurences[polymer[idx]] += 1 
        element_occurences[polymer[idx + 1]] += 1         


    print(element_occurences)

    # Now loop and begin the process of replacement. 
    for iteration in range(iterations):
        new_polymer_occurences = defaultdict(int)
        for elem, instances in polymer_occurences.items(): 
            if elem in polymer_substitution:
                # We need to do replacement on this.
                # AB -> C
                # AB: 5 
                # AC: AC + 5 
                # CB: CB + 5 

                first_pair = elem[0] + polymer_substitution[elem]
                second_pair = polymer_substitution[elem] + elem[1]

                new_polymer_occurences[first_pair] += polymer_occurences.get(elem)
                new_polymer_occurences[second_pair] += polymer_occurences.get(elem)


                element_occurences[polymer_substitution[elem]] += polymer_occurences.get(elem)

                # new_polymer_occurences[first_pair] = polymer_occurences.get(first_pair) + polymer_occurences.get(elem)
            else: 
                if elem not in new_polymer_occurences:
                    new_polymer_occurences[elem] = polymer_occurences[elem]

        print(f"{iteration} | {iteration / iterations * 100}%")



        polymer_occurences = new_polymer_occurences

    print("Done!")
    print(polymer_occurences)
    print(element_occurences)

    return element_occurences





print(polymer_template)
print(polymer_substitution)


# built_polymer = build_polymer(40, polymer_template, polymer_substitution)
built_polymer = build_polymer_better(40, polymer_template, polymer_substitution)
res = solve_problem(built_polymer)
print(res)

