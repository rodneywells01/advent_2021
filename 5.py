vents = dict()
def record_vent(start, end):
	num_vents = max(abs(end[1] - start[1]), abs(end[0] - start[0])) + 1
	direction_x = int((end[0] - start[0])/(num_vents - 1))
	direction_y = int((end[1] - start[1])/(num_vents - 1))
	
	for idx in range(num_vents):
		# Create a key of the format "y,x" for a vent. 
		key = f"{start[1] + idx * direction_y},{start[0] + idx * direction_x}"

		if vents.get(key):
			vents[key] += 1
		else: 
			vents[key] = 1
		
def count_multiple_vents(): 
	return sum([num_vents > 1 for num_vents in vents.values()])
	

with open('input/5.txt') as f:
	lines = f.readlines()

	for line in lines:
		vent_coordinates = line.rstrip().split()
		start = [int(coordinate) for coordinate in vent_coordinates[0].split(",")]
		end = [int(coordinate) for coordinate in vent_coordinates[2].split(",")]

		record_vent(start, end)

	total = count_multiple_vents()
	print(f"Total: {total}")
	# assert total == 18144
