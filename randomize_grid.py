from random import randint, shuffle, choice
import numpy as np

def randomize_grid(size):
	line = [i for i in range(1, size + 1)]
	grid = []
	grid.append(line)
	for i in range(size - 1):
		line = [line[-1]] + line[0:size-1]
		grid.append(line)
	for i in range(size):
		shuffle(grid)
	grid = list(np.transpose(grid))
	for i in range(size):
		shuffle(grid)
	return grid

def randomize_cages(grid):
	cages = []
	size = len(grid)
	caged_state = np.zeros_like(grid)
	for row in range(size):
		for col in range(size):
			if(caged_state[row][col] == 0):
				caged_state[row][col] = 1
				curr_cage = []
				curr_cage.append((row, col))
				cage_size = randint(1, 4)
				for i in range(cage_size - 1):
					pos_row, pos_col = choice(curr_cage)
					neighbours = []
					if(pos_col >= 1): neighbours.append((pos_row, pos_col - 1))
					if(pos_col < size - 1): neighbours.append((pos_row, pos_col + 1))
					if(pos_row >= 1): neighbours.append((pos_row - 1, pos_col))
					if(pos_row < size - 1): neighbours.append((pos_row + 1, pos_col))
					shuffle(neighbours)
					for neigh_row, neigh_col in neighbours:
						if(caged_state[neigh_row][neigh_col] == 0):
							caged_state[neigh_row][neigh_col] = 1
							curr_cage.append((neigh_row, neigh_col))
							break
				if(len(curr_cage) > 2):
					op = choice(["add", "mult"])
				elif(len(curr_cage) == 2):
					op = choice(["add", "sub", "mult", "div"])
				else:
					op = "add"
				if(op == "add"):
					res = 0
					for i,j in curr_cage:
						res += grid[i][j]
				elif(op == "mult"):
					res = 1
					for i,j in curr_cage:
						res *= grid[i][j]
				elif(op == "sub"):
					res = abs(grid[curr_cage[0][0]][curr_cage[0][1]] - grid[curr_cage[1][0]][curr_cage[1][1]])
				else: # op == "div"
					if (grid[curr_cage[0][0]][curr_cage[0][1]] % grid[curr_cage[1][0]][curr_cage[1][1]] == 0):
						res = grid[curr_cage[0][0]][curr_cage[0][1]] // grid[curr_cage[1][0]][curr_cage[1][1]]
					elif(grid[curr_cage[1][0]][curr_cage[1][1]] % grid[curr_cage[0][0]][curr_cage[0][1]] == 0):
						res = grid[curr_cage[1][0]][curr_cage[1][1]] // grid[curr_cage[0][0]][curr_cage[0][1]]
					else:
						op = choice(["add", "sub", "mult"])
						if(op == "add"):
							res = 0
							for i,j in curr_cage:
								res += grid[i][j]
						elif(op == "mult"):
							res = 1
							for i,j in curr_cage:
								res *= grid[i][j]
						elif(op == "sub"):
							res = abs(grid[curr_cage[0][0]][curr_cage[0][1]] - grid[curr_cage[1][0]][curr_cage[1][1]])
				cages.append((curr_cage, op, res))
	return cages

if __name__ == "__main__":
	size = 5
	grid = randomize_grid(size)
	print(np.array(grid))
	print(np.array(randomize_cages(grid)))
