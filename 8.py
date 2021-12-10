

def parse_input():
    # Parse file input

    output_values = []
    signal_patterns = []

    with open("input/8.txt") as f:
        lines = f.readlines()

        for line in lines:
            pieces = line.split("|")
            output_values.append(
                pieces[1].rstrip().split()
            )
            signal_patterns.append(
                pieces[0].split()
            )

    return signal_patterns, output_values


def solve_part_one():
    # 1, 4, 7, or 8
    num_parts = {
        1: 2,
        4: 4, 
        7: 3,
        8: 7
    }
    valid_sizes = set([2, 4, 3, 7])

    output_values = parse_input()[1]

    num_appearances = 0
    for output in output_values: 
        for output_code in output:
            if len(output_code) in valid_sizes:
                num_appearances += 1

    print(f"found {num_appearances} instances of 1,4,7,8")


def decode_individual_code(code): 
    values = {
        "abcefg": 0, 
        "cf": 1,
        "acdeg": 2, 
        "acdfg": 3,
        "bcdf": 4, 
        "abdfg": 5, 
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8, 
        "abcdfg": 9    
    }

    return values[code]

def decode_output(corrected_mapping, output):
    final_output = ""

    print("DECODING OUTPUT")
    for output_code in output: 
        output_code = list(output_code)
        output_code.sort()
        output_code = ''.join(output_code)
        print(output_code)

        print(corrected_mapping) 
        print(output_code)

        try:
            converted_number = corrected_mapping[output_code]
            final_output += str(converted_number)
        except KeyError as ke: 
            raise KeyError("We failed to properly determine the code!")

        

    return int(final_output)



def solve_part_two(): 
    signal_patterns, output_values = parse_input()

    size_to_num = {
        2: 1,
        4: 4, 
        3: 7,
        7: 8
    }

    # Let's start with just one 
    # signal_patterns = signal_patterns[:1]
    


    final_outputs = []
    for signal_pattern, output_value in zip(signal_patterns, output_values):
        char_count = {char: 0 for char in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
        corrected_mapping = {char: None for char in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
        reverse_corrected_mapping = {char: None for char in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
        nums_to_chars = {num:None for num in range(10)}
    
        # Start by decoding the uniquely sized numbers (1,4,7,8)
        found_count = 0 
        for signal in signal_pattern:
            print(signal)

            for char in signal:
                char_count[char] += 1

            if len(signal) in size_to_num: 
                found_count += 1
                for char in signal:
                    nums_to_chars[size_to_num[len(signal)]] = set(signal)

        if found_count != 4: 
            raise Exception("We failed to find a known number!")

        print(char_count)
        found_nine = False
        found_four = False
        for char, count in char_count.items(): 
            # E only appears 4 times 
            # F only appears 9 times 
            if count == 9:
                corrected_mapping['f'] = char
                reverse_corrected_mapping[char] = 'f'
                found_nine = True
            elif count == 4:
                corrected_mapping['e'] = char
                reverse_corrected_mapping[char] = 'e'
                found_four = True 

        if not all([found_four, found_nine]):
            raise Exception("We couldn't find something")
                    
        # Decode top of 7 
        a_value = next(iter(nums_to_chars[7].difference(nums_to_chars[1])))
        corrected_mapping['a'] = a_value
        reverse_corrected_mapping[a_value] = 'a'

        # We can decode the value of c from 1 now that we know the value of f. 
        value_of_c = next(iter(nums_to_chars[1].difference(set([corrected_mapping['f']]))))
        corrected_mapping['c'] = value_of_c
        reverse_corrected_mapping[value_of_c] = 'c'


        # Find 9. 
        for signal in signal_pattern: 
            if len(signal) == 6:
                if corrected_mapping['e'] not in signal: 
                    nums_to_chars[9] = set(signal)
                    break

        # Find 0 and 6 by our information on 9 and what is truly 'e'
        found_6 = False
        found_0 = False 
        print("CORRECTED MAPPING")
        for key, val in corrected_mapping.items():
            print(f"{key}: {val}")
        print("REVERSE CORRECTED MAPPING")
        for key, val in reverse_corrected_mapping.items():
            print(f"{key}: {val}")

        for signal in signal_pattern: 
            if len(signal) == 6: 
                set_signal = set(signal)
                nine_minus_other = nums_to_chars[9].difference(set_signal)
                if len(nine_minus_other) == 1:
                    difference = set_signal.difference(nums_to_chars[9])
                    if len(difference) == 1:
                        print("Found a single difference!")
                        diff = next(iter(nine_minus_other))
                        print(diff)
                        if diff == corrected_mapping['c']:
                            print("WE FOUND 6!")
                            nums_to_chars[6] = set_signal
                            found_6 = True

                        else: 
                            print("WE FOUND 0!")

                            # This tells us the true value of d 
                            nums_to_chars[0] = set_signal
                            corrected_mapping['d'] = diff
                            reverse_corrected_mapping[diff] = 'd'
                            found_0 = True


        if not all([found_0, found_6]):
            raise Exception("We failed to find something!")

        # At this point we should have found the following: 
        # 1,4,7,8, 9, 0, 6
        print("FIND CHECK")
        for key, val in nums_to_chars.items():
            print(f"{key}: {val}")


        # Collect 2,3,5 from the signals
        current_numbers = nums_to_chars.values()
        final_unknowns = [] 
        for signal in signal_pattern:
            if set(signal) not in current_numbers: 
                final_unknowns.append(set(signal))

        if len(final_unknowns) != 3: 
            print(final_unknowns)
            raise Exception("There are more than 3 final_unknowns!")


        print("HERE'S WHAT WE'VE GOT LEFT")
        print(final_unknowns)
        for signal in final_unknowns: 
            diff = signal.difference(nums_to_chars[4])
            if len(diff) == 2: 
                # We can find G off of this. It's either 3 or 5 (a or g). 
                print("Here")
                print(diff)
                value_of_g = next(iter(diff.difference(corrected_mapping['a'])))
                corrected_mapping['g'] = value_of_g
                reverse_corrected_mapping[value_of_g] = 'g'

                # Since we're only short b, it's the only other unknown. 
                for incorrect_char, corrected_char in reverse_corrected_mapping.items(): 
                    if not corrected_char: 
                        # We found the value 'b'. 
                        corrected_mapping['b'] = incorrect_char
                        reverse_corrected_mapping[incorrect_char] = 'b' 
                        break 

        # We now know the value of every char.
        # Conver the unkonwns into knowns. 
        for signal in final_unknowns: 
            converted_code = set([reverse_corrected_mapping[incorrect_char] for incorrect_char in signal])
            print(f"Convert {signal} into {converted_code}")
            str_converted_code = list(converted_code)
            str_converted_code.sort()
            num = decode_individual_code(''.join(str_converted_code))
            nums_to_chars[num] = signal


        print("CORRECTED")
        for key, val in corrected_mapping.items():
            print(f"{key}: {val}")

        print("NUMS_TO_CHARS")
        for key, val in nums_to_chars.items():
            print(f"{key}: {val}")

        #  Build a lookup mapping to easily decode output
        lookup_mapping = {}
        for code, chars in nums_to_chars.items():
            # print(chars)
            chars = list(chars)
            chars.sort()
            lookup_mapping[''.join(chars)] = code

        print("LOOKUP MAPPING:")
        print(lookup_mapping)
        res = decode_output(lookup_mapping, output_value)

        print(f"FINAL OUTPUT: {res}")

        final_outputs.append(res)


    print(final_outputs)
    print(sum(final_outputs))



def display_current_puzzle_info(signal_pattern, output_value, corrected_mapping, reverse_corrected_mapping): 
    print(f"Signal Pattern: {signal_pattern}")
    print(f"Output Value: {output_value}")

    print("CORRECTED MAPPING")
    for key, val in corrected_mapping.items():
        print(f"{key}: {val}")

    print("REVERSE CORRECTED MAPPING")
    for key, val in reverse_corrected_mapping.items():
        print(f"{key}: {val}")


solve_part_one()
solve_part_two()