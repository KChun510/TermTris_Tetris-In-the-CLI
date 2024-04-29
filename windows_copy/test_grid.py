"""
The length of the grid is 66. There are 66 rows, and every + 1 row contains the cells


"""
grid = []
empty = '   '
fill = u"\u2588\u2588\u2588"



box = ["*---* ", f"|{empty}| ", "*---* "]
for row in range(22):
	for box_line in box:
		grid += [[box_line] * 10]


grid[64] = [ f"|{fill}| "] * 10

for row in grid:
	print(row)


print(len(grid))



row = 0
while row < 66:
	if grid[row] == [ f"|{fill}| "] * 10:
		print('THIS IS TRUE!!!!')

	row += 1
