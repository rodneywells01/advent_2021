class BingoGame(): 
	def __init__(self, numbers, boards=[]):
		self.boards = boards 
		self.win_status = dict() 
		self.winners = []
		self.numbers = numbers
		self.current_number = 0 


	def play(self):
		#  Play as long as there are numbers to call. 
		for number in self.numbers:
			print(f"Testing {number}")
			winner = self.play_move(number)
			if winner: 
				print("There's a winner")

				# Calculate the final score. 
				total_uncalled = 0 
				for row_idx in range(len(winner.board)):
					for col_idx in range(len(winner.board)):
						if not winner.marked_grid[row_idx][col_idx]:
							uncalled_value = int(winner.board[row_idx][col_idx])
							print(f"Adding {uncalled_value} to {total_uncalled}")
							total_uncalled += uncalled_value

				print(total_uncalled)
				final_score = total_uncalled * int(number)
				print(f"The final score is {final_score}!")
				return final_score

			print(f"{len(self.winners)} Winners out of {len(self.boards)} boards")

		print ("We ran out of numbers!")
		return None


	def play_move(self, number):
		for idx in range(len(self.boards)): 
			new_winner = False 
			if not self.boards[idx].winner:
				new_winner = self.boards[idx].play_move(number)

			if new_winner:
				if len(self.winners) == len(self.boards) - 1:
					# We found our last winning board!
					return self.boards[idx]
					
				self.winners.append(idx)
		return None 

	def check_winner(self): 
		for board in self.boards: 
			if board.check_winner():
				return board 

		return None

class BingoBoard(): 
	def __init__(self, board): 
		self.board = board
		self.num_to_location = dict() 
		self.marked_grid = [[False for _ in range(5)] for _ in range(5)]

		self.diag1 = [[x,x] for x in range(5)]
		self.diag2 = [[4-x, x] for x in range(5)]
		self.winner = False

		for row_idx in range(len(board)): 
			for col_idx in range(len(board[row_idx])): 
				number = board[row_idx][col_idx]
				self.num_to_location[number] = [row_idx, col_idx]


	def play_move(self, number): 
		location = self.num_to_location.get(number)

		if location:
			self.marked_grid[location[0]][location[1]] = True

			# Check winner status. 
			winner = any([
				all(self.marked_grid[location[0]]),
				all([self.marked_grid[row_col][location[1]] for row_col in range(5)]),
				all([self.marked_grid[x[0]][x[1]] for x in self.diag1]),
				all([self.marked_grid[x[0]][x[1]] for x in self.diag2])
			])


			# winner = all(self.marked_grid[location[0]]) 
			# print(self.marked_grid[location[0]])

			if winner:
				print("Board won!")
				print(self.marked_grid)
				print(self.board)
				self.winner = True 

			return winner

		return None



with open('input/4.txt') as f:
    lines = f.readlines()
    numbers = lines[0].rstrip().split(",")
    idx = 2
    boards = []
    while idx <= len(lines):
    	# The next 5 lines will be a board 
    	board = lines[idx:idx+5]
    	formatted_board = []
    	for row in board:
    		formatted_board.append(row.rstrip().split())

    	boards.append(
    		BingoBoard(formatted_board)
		)

    	idx += 6


    game = BingoGame(numbers, boards)
    winner = game.play()


numbers = [15,62,2,39,49,25,65,28,84,59,75,24,20,76,60,55,17,7,93,69,32,23,44,81,8,67,41,56,43,89,95,97,61,77,64,37,29,10,79,26,51,48,5,86,71,58,78,90,57,82,45,70,11,14,13,50,68,94,99,22,47,12,1,74,18,46,4,6,88,54,83,96,63,66,35,27,36,72,42,98,0,52,40,91,33,21,34,85,3,38,31,92,9,87,19,73,30,16,53,80]
