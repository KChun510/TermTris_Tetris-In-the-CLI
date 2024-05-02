import os, time
import threading




peice_pos = [0,0]
lock = threading.Lock()
grid = []
last_move = []  # We will keep a tempory trace of the index's are filled. Needed for peice deletion
taken_cell = []
peice_alive = 1
count = 0
user_input = ""
game_alive = True
cell_taken_flag = False
cleard_row = []
max_game_count = 250


class grid_field:
	def __init__(self):
		global grid
		self.length = 10
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
		#for row in grid[6:]:
		for row in grid[:]:
			print(''.join(row))

class peice():
	def __init__(self):
		global grid
		global peice_pos
		global last_move
		global cardinal
		cardinal = ''
		#grid = grid_arr
		#self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"


		#peice_pos = [0,0] # y, x
		peice_pos = [10, 4]
		#peice_pos = [10 , 5]


	def show_grid(self):
		os.system('cls||clear')
		#for row in grid[6:]:
		for row in grid[:]:
			print(''.join(row))


	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		peice_pos = self.center
		grid[peice_pos[0]][peice_pos[1]] = f"|{self.fill}| "
	

	def check_grid(self) -> bool:
		global grid
		global taken_cell
		global peice_alive
		global cleard_row
		clear_flag = 0
		clear_count = 0
		row = 64


		# Evaluate, clear, drop row, re-evaluate
		while row > 2:
			if grid[row] == [ f"|{self.fill}| "] * 10:
				clear_flag = 1
				clear_count += 1
				grid[row] = [f"|{self.empty}| "] * 10

				cleard_row += [row]
				tmp_array = []
				for val in taken_cell:
					if val[0] == row:
						pass
					else:
						# This does 2 things. One, save the cells we want to drop down. 
						# Two, update the taken cells to match the clear
						tmp_array += [[val[0] + 3, val[1]]]

				taken_cell = tmp_array
				tmp = row
				while tmp > 2:
					grid[tmp] = grid[tmp - 3].copy()
					tmp -= 3

				row = 64

			else:
				row -= 3

		return True








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
		for cord in last_move:
			if [cord[0] + 3, cord[1]] in taken_cell:
				return True

		return False



	# Because python threads dont in true parrell. This function checks two space ahead
	# TO make up for the un-synced position across threads
	def is_cell_taken_force(self) -> bool:
		global taken_cell
		global last_move
		for cord in last_move:
			if [cord[0] + 6, cord[1]] in taken_cell or [cord[0] + 3, cord[1]] in taken_cell:

				return True

		return False



	def fill_cell(self, y: int, x:int) -> None:
		global grid
		print(y, x)
		if y <= 64: 
			grid[y][x] = f"|{self.fill}| "
		else:
			grid[64][x] = f"|{self.fill}| "
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
		global game_alive
		collision_flag_block = 0
		collision_flag_floor = 0


		tmp = last_move.copy()
		# Check if we are out of our top bound

		if peice_alive == 0:
			return False

		if (self.is_cell_taken()):
			"""
			lock.acquire()
			collision_flag_block = 1
			lock.release()
			"""
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
			

		if len(last_move) > 0:
			for cord in tmp: 
				if (cord[0] >= 64):
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

		for cord in last_move:
			if (cord[0] < 7 and self.is_cell_taken()):
				game_alive = False
				return False
		

		
		return True


	# Can add extra logic here to account for set blocks on the bottom
	def move_down(self) -> None: # Moves our block down one space at a time
		global peice_pos
		global last_move
		global next_cells
		global user_input


		tmp = last_move.copy()


		if self.check_pos():
			# Extra condition, to ensure not moving out of grid
			if len(last_move) > 0:
				# This is how we sink the data between threads.
				# Make up for the incrimented value in our counter func
				# Only move down if value was updated
				delta =  peice_pos[0] - last_move[0][0]
				if delta > 3 and user_input != 's':
					delta = 3

		 		
				
				self.remove_peice() 
				for cord in tmp:
					self.fill_cell(cord[0] + delta , cord[1])
					last_move += [[cord[0] + delta , cord[1]]]
		else:
			lock.acquire()
			peice_alive =  0
			lock.release()
			self.show_grid()






	
	def move_left(self) -> None:
		global peice_pos
		global last_move
		global next_cells
		global cardinal

		
		tmp = last_move.copy()
		for cord in tmp:
			if cord[1] == 0:
				self.move_down()
				return None
			elif [cord[0] ,cord[1] - 1] in taken_cell or [cord[0] + 3 ,cord[1] - 1] in taken_cell :
				self.move_down()
				return None

		if self.check_pos():

			if ((peice_pos[1] > 0 and cardinal != 'west') or (cardinal == 'west' and peice_pos[1] > 3)):
				peice_pos = [peice_pos[0], peice_pos[1] - 1]

				self.remove_peice() 
				for cord in tmp:
					self.fill_cell(cord[0], cord[1] - 1)
					last_move += [[cord[0], cord[1] - 1]]

			else:
				self.move_down()
		else:
			self.move_down()

	
	def move_right(self) -> None:
		global peice_pos
		global last_move
		global next_cells
		global taken_cell
		global cardinal	

 

		
		tmp = last_move.copy()
		
		for cord in tmp:
			if cord[1] == 9:
				self.move_down()
				return None
			elif [cord[0] ,cord[1] + 1] in taken_cell or [cord[0] + 3,cord[1] + 1] in taken_cell:
				self.move_down()
				return None

		if self.check_pos():
			

			if ((peice_pos[1] < 9 and cardinal != 'east') or (cardinal == 'east' and peice_pos[1] < 6)):
				peice_pos = [peice_pos[0], peice_pos[1] + 1]

				self.remove_peice() 
				for cord in tmp:
					
					self.fill_cell(cord[0], cord[1] + 1)
					last_move += [[cord[0], cord[1] + 1]]

			else:
				self.move_down()

		else:
			self.move_down()

	def force_down(self) -> None:
		global peice_pos
		if peice_pos[0] < 64 and not self.is_cell_taken_force():
			lock.acquire()
			peice_pos[0] += 3
			lock.release()
			self.move_down()





	def rotate(self) -> None:
		global last_move
		global grid
		length = 4
		count = 1
		#last_move = last_move[::-1]

		tmp = last_move.copy()
		self.remove_peice()
		for cord in tmp:
			cord = cord[::-1]
			self.fill_cell((cord[0] * 3) + 1, cord[1] // 3)
			last_move += [[(cord[0] * 3) + 1, cord[1] // 3]]
		
		self.show_grid()
		print(tmp)







"""
Moving forward we are going to use a sinlgle block to track position and movement
Think of the center peice/when we were only moving around a single block

"""
class peice_L_block(peice):
	def __init__(self):
		peice.__init__(self)
		global last_move
		global peice_pos
		global grid
		

		"""
		lock.acquire()
		#peice_pos = self.center
		lock.release()
		"""
		self.length = 4


		last_move = [] # We will keep a tempory trace of the index's are filled. Needed for peice deletion
		#print(peice_pos)
		# peice_pos[0] += 3
		lock.acquire()
		peice_pos = peice_pos
		self.tmp = peice_pos.copy()
		lock.release()
	

		for cell in range(self.length):
			grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
		
			last_move += [[self.tmp[0],self.tmp[1]]]
			#next_cells += [[self.tmp[0] + 3,self.tmp[1]]]

			if cell == 3:
				grid[self.tmp[0]][self.tmp[1]+1] = f"|{self.fill}| "
				last_move += [[self.tmp[0],self.tmp[1] + 1]]

			self.tmp[0] += 3

		self.show_grid()




"""

class peice_o_block(peice):
	def __init__(self):
		peice.__init__(self)
		global last_move
		global peice_pos
		global grid
		


		self.length = 2


		last_move = [] # We will keep a tempory trace of the index's are filled. Needed for peice deletion
		#print(peice_pos)
		# peice_pos[0] += 3
		lock.acquire()
		peice_pos = peice_pos
		self.tmp = peice_pos.copy()
		lock.release()
	
		for cell in range(self.length):
			grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
			grid[self.tmp[0] + 3][self.tmp[1]] = f"|{self.fill}| "
			last_move += [[self.tmp[0],self.tmp[1]]]
			last_move += [[self.tmp[0] + 3,self.tmp[1]]]
			#next_cells += [[self.tmp[0] + 3,self.tmp[1]]]
		
			self.tmp[1] += 1

		self.show_grid()
	



"""




def main():
	global grid
	global last_move
	peice_control = peice()
	grid_control = grid_field()
	grid_control.show_grid()
	#o_block = peice_O_block()
	l_block = peice_L_block()
	print(last_move)
	time.sleep(2)
	l_block.rotate()
	print(last_move)


	print(f"The width is: {len(grid[0])}")
	print(f"The length is: {len(grid)}")
	
	"""

	obj = MyClass()
	try:
	    func = getattr(obj, "dostuff")
	    func()
	except AttributeError:
	    print("dostuff not found")
		
	#print(grid)

	"""

if __name__ == "__main__":
	main()
