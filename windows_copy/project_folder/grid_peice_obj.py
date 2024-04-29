class grid_field:
	def __init__(self):
		global grid
		self.length = 22
		self.width = 10
		self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"

		# This var, may have to stem fm parent class.
		# Idea in order for our decrement(Going down), we'll need to keep track of the center pos
		#peice_pos = [0,0] # y, x
	

		box = ["*---* ", f"|{self.empty}| ", "*---* "]
		for row in range(self.length):
			for box_line in box:
				grid += [[box_line] * self.width]

		self.length = len(grid) - 1 

	def show_grid(self):
		os.system('cls||clear')
		for row in grid[2:]:
			print(''.join(row))

	
class peice():
	def __init__(self):
		global grid
		global peice_pos
		global last_move
		#grid = grid_arr
		#self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"


		#peice_pos = [0,0] # y, x
		peice_pos = [1 , 5]


	def show_grid(self):
		os.system('cls||clear')
		for row in grid:
			print(''.join(row))


	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		peice_pos = self.center
		grid[peice_pos[0]][peice_pos[1]] = f"|{self.fill}| "
	

	def check_block_top(self) -> bool:
		global peice_pos
		global grid
		"""
		print(f"This is the center value {peice_pos}")
		print(f"This should be filled {grid[peice_pos[0]][peice_pos[1]]}")
		print(f"Make sure this is filled: {grid[peice_pos[0] + 3][peice_pos[1]]}")
		time.sleep(1)
		"""
		if (grid[peice_pos[0] - 3][peice_pos[1]] == f"|{self.fill}| "):
			return True
		else:
			return False


	def check_block_left(self) -> bool:
		global peice_pos
		global grid
		"""
		print(f"This is the center value {peice_pos}")
		print(f"This should be filled {grid[peice_pos[0]][peice_pos[1]]}")
		print(f"Make sure this is filled: {grid[peice_pos[0] + 3][peice_pos[1]]}")
		time.sleep(1)
		"""
		if (grid[peice_pos[0]][peice_pos[1] - 1] == f"|{self.fill}| "):
			return True
		else:
			return False	

	def check_block_right(self) -> bool:
		global peice_pos
		global grid
		
		"""
		print(f"This is the center value {peice_pos}")
		print(f"This should be filled {grid[peice_pos[0]][peice_pos[1]]}")
		print(f"Make sure this is filled: {grid[peice_pos[0] + 3][peice_pos[1]]}")
		time.sleep(1)
		"""
		if (grid[peice_pos[0]][peice_pos[1] + 1] == f"|{self.fill}| "):
			return True
		else:
			return False


	def check_block_under(self) -> bool:
		global peice_pos
		global grid
		"""
		print(f"This is the center value {peice_pos}")
		print(f"This should be filled {grid[peice_pos[0]][peice_pos[1]]}")
		print(f"Make sure this is filled: {grid[peice_pos[0] + 3][peice_pos[1]]}")
		time.sleep(1)
		"""
		if (grid[peice_pos[0] + 3][peice_pos[1]] == f"|{self.fill}| "):
			return True
		else:
			return False

	def is_cell_taken(self) -> bool:
		global taken_cell
		global last_move
		tmp = last_move.copy()
		for cord in tmp:
			if [cord[0] + 3, cord[1]] in taken_cell:
				return True
		return False



	def fill_cell(self, y: int, x:int) -> None:
		global grid
		if y <= 58: 
			grid[y][x] = f"|{self.fill}| "
		else:
			grid[58][x] = f"|{self.fill}| "
		return None



	"""
	def remove_peice(self):
		grid[peice_pos[0]][peice_pos[1]] = f"|{self.empty}| "
	"""
	
	def move_pos_y(self):
		if (peice_pos[0] >= 3 and peice_pos[0] <= self.length - 1):
			self.remove_peice()
			peice_pos[0] -= 3
			self.place_peice()
	
	def move_neg_y(self):
		if (peice_pos[0] >= 0 and peice_pos[0] < self.length - 1):
			self.remove_peice()
			peice_pos[0] += 3
			self.place_peice()

	def move_pos_x(self):
		if (peice_pos[1] >= 0 and peice_pos[1] < self.width - 1):
			self.remove_peice()
			peice_pos[1] += 1
			self.place_peice()
	
	def move_neg_x(self):
		if (peice_pos[1] > 0 and peice_pos[1] <= self.width - 1):
			self.remove_peice()
			peice_pos[1] -= 1
			self.place_peice()




	def remove_peice(self) -> None:
		global last_move
		global grid
		tmp = last_move.copy()
		last_move = []
		if self.check_pos():
			for cords in tmp:
				grid[cords[0]][cords[1]]  = f"|{self.empty}| "
			



	def is_peice_alive(self) -> bool:
		global peice_alive
		if peice_alive:
			return True
		else:
			False

			
	def check_pos(self) -> bool: 
		global last_move
		global peice_pos
		global taken_cell
		global peice_alive
		collision_flag_block = 0
		collision_flag_floor = 0


		tmp = last_move.copy()

		if (self.is_cell_taken()):
			print("Collision detected")
			lock.acquire()
			collision_flag_block = 1
			lock.release()

		if len(last_move) > 0:
			for cord in tmp: 
				if (cord[0] >= 58):
					collision_flag_floor = 1
					break
		
		if peice_alive == 0:
			return False
			
		if collision_flag_floor == 1 and collision_flag_block == 1:
			for cord in tmp:
				self.fill_cell(cord[0] , cord[1])
				taken_cell += [[cord[0], cord[1]]]
		
			self.show_grid()
		
			lock.acquire()
			last_move = []
			peice_pos = [1, 5]
			peice_alive = 0
			lock.release()

			return False

		

		elif collision_flag_floor == 1:
			#self.remove_peice()
			for cord in tmp:
				self.fill_cell(cord[0], cord[1])
				taken_cell += [[cord[0], cord[1]]]

			self.show_grid()
			
			lock.acquire()
			last_move = []
			peice_pos = [1, 5]
			peice_alive = 0
			lock.release()
			
			return False


		elif collision_flag_block == 1:
			for cord in tmp:
				self.fill_cell(cord[0] , cord[1])
				taken_cell += [[cord[0], cord[1]]]
		
			self.show_grid()
		
			lock.acquire()
			last_move = []
			peice_pos = [1, 5]
			peice_alive = 0
			lock.release()
			
			
			return False
		else:
			return True


	
		


	# Can add extra logic here to account for set blocks on the bottom
	def move_down(self) -> None: # Moves our block down one space at a time
		global peice_pos
		global last_move
		global next_cells


		lock.acquire()
		peice_pos = peice_pos
		tmp = last_move.copy()
		lock.release()

		print("Were moving down ")

		# Extra condition, to ensure not moving out of grid
		if len(last_move) > 0 and last_move[0][0] < 58:
			# This is how we sink the data between threads.
			# Make up for the incrimented value in our counter func
			# Only move down if value was updated
			delta =  peice_pos[0] - last_move[0][0]
		else:
			delta = 0
 	
		print("Move down")
		if self.check_pos():
			self.remove_peice() 
			for cord in tmp:
				self.fill_cell(cord[0] + delta , cord[1])
				last_move += [[cord[0] + delta , cord[1]]]

				"""
				if cord[0] >= 58: # In case we reached our maxed bounds
					self.fill_cell(cord[0] , cord[1])
					last_move += [[cord[0] , cord[1]]]
				else:
					self.fill_cell(cord[0] + delta , cord[1])
					last_move += [[cord[0] + delta , cord[1]]]
				"""
		else:
			lock.acquire()
			peice_alive =  0
			lock.release()
			self.show_grid()




	def move_down_manual(self) -> None: # Moves our block down one space at a time
		global peice_pos
		global last_move
	
		tmp = last_move.copy()
		self.remove_peice()
		print(f"The actual position {peice_pos}")
		peice_pos[0] += 3

		for cords in tmp: 
			grid[cords[0] + 3][cords[1]]  = f"|{self.fill}| "
			last_move += [[cords[0] + 3, cords[1]]]
		next_cells = []	
		return None