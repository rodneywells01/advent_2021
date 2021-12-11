def parse_input():
    # Parse file input
    lines = []
    with open("input/10.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]

    return lines 



lines = parse_input()
print(lines)


left_facing_chars = set(["(", "[", "{", "<"])
right_facing_chars = set([")", "]", "}", ">"]) 

matching_closing_char_map = {
	"(": ")",
	"[": "]",
	"{": "}",
	"<": ">"
}

char_error_score = {
	")": 3,
	"]": 57,
	"}": 1197,
	">": 25137,
}

missing_char_score = {
	")": 1,
	"]": 2,
	"}": 3,
	">": 4
}


total_error_score = 0 
incomplete_lines = []
incomplete_scores = []
for line in lines: 
	print(line)

	stack = []
	corrupt = False 
	for current_char in line:
		if current_char in left_facing_chars: 
			stack.append(current_char)

		elif current_char in right_facing_chars:
			match_char = stack.pop()
			print(f"{match_char} {current_char} ")

			if matching_closing_char_map[match_char] != current_char:
				print("Corrupted line!")
				total_error_score += char_error_score[current_char]
				corrupt = True 
				break

	if not corrupt:
		# This line needs to be completed. 
		score = 0 
		for char in reversed(stack): 
			score *= 5 
			required_matching_char = matching_closing_char_map[char]
			score += missing_char_score[required_matching_char]

		print(f"This line had {score} score for completion")
		incomplete_scores.append(score)


# Grab the middle score. 
incomplete_scores.sort() 
print(incomplete_scores)
middle_score = incomplete_scores[int(len(incomplete_scores) / 2)]
print(middle_score)

