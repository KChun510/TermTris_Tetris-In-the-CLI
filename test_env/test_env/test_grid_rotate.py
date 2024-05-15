from pynput import keyboard
#import msvcrt # Windows
import os
import time
import threading
import random
import math


lock = threading.Lock()
peice_pos = [0,0]
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
		self.length = 24
		self.width = 10
		self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"
		# Idea in order for our decrement(Going down), we'll need to keep track of the center pos
		#peice_pos = [0,0] # y, x
		box = ["*---* ", f"|{self.empty}| ", "*---* "]
		for row in range(self.length):
			for box_line in box:
				grid += [[box_line] * self.width]

		self.length = len(grid) - 1 

	def show_grid(self):
		os.system('cls||clear')
		for row in grid[12:]:
		#for row in grid[:]:
			print(''.join(row))

class peice():
	def __init__(self):
		global grid
		global peice_pos
		global last_move
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"
		#peice_pos = [0,0] # y, x
		#peice_pos = [10, 0]
		peice_pos = [4 , 4]
		#peice_pos = [25 , 5]
	def show_grid(self):
		os.system('cls||clear')
		#for row in grid[6:]:
		for row in grid[12:]:
			print(''.join(row))


	def place_center(self):
		peice_pos = self.center
		grid[peice_pos[0]][peice_pos[1]] = f"|{self.fill}| "
	

	def check_grid(self) -> bool:
		global grid
		global taken_cell
		global peice_alive
		global cleard_row
		clear_flag = 0
		clear_count = 0
		row = 70


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

				row = 70

			else:
				row -= 3

		return True

	def is_cell_taken_bellow(self) -> bool:
		global taken_cell
		global last_move
		for cord in last_move:
			if [cord[0] + 3, cord[1]] in taken_cell:
				return True
		return False

	def is_cell_taken_right(self) -> bool:
		global taken_cell
		global last_move
		for cord in last_move:
			if [cord[0], cord[1] + 1] in taken_cell:
				return True
		return False

	def is_cell_taken_left(self) -> bool:
		global taken_cell
		global last_move
		for cord in last_move:
			if [cord[0], cord[1] - 1] in taken_cell:
				return True
		return False

	def fill_cell(self, y: int, x:int) -> None:
		global grid
		if y <= 70: 
			grid[y][x] = f"|{self.fill}| "
		else:
			grid [70][x] = f"|{self.fill}| "
		return None

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
		if peice_alive == 0:
			return False


		# If there is a taken cell bellow
		if (self.is_cell_taken_bellow()):
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
			
		# Floor collision
		if len(last_move) > 0:
			for cord in tmp: 
				if (cord[0] >= 70):
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

		# End game condition
		for cord in last_move:
			if (cord[0] < 7 and self.is_cell_taken_bellow()):
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

				self.show_grid()

		else:
			lock.acquire()
			peice_alive =  0
			lock.release()
			self.show_grid()

	
	def move_left(self) -> None:
		global peice_pos
		global last_move

		tmp = last_move.copy()
		
		for cord in tmp:
			if cord[1] - 1 < 0:
				return None


		if (self.check_pos() and not self.is_cell_taken_left()):

			peice_pos = [peice_pos[0], peice_pos[1] - 1]

			self.remove_peice() 
			for cord in tmp:
				self.fill_cell(cord[0], cord[1] - 1)
				last_move += [[cord[0], cord[1] - 1]]
		else:
			self.move_down()

	
	def move_right(self) -> None:
		global peice_pos
		global last_move

		tmp = last_move.copy()
		
		# Checking if right move it out of bounds
		for cord in tmp:
			if cord[1] + 1 > 9:
				return None
		if(self.check_pos() and not self.is_cell_taken_right()):	
			peice_pos = [peice_pos[0], peice_pos[1] + 1]
			self.remove_peice() 
			for cord in tmp:
				self.fill_cell(cord[0], cord[1] + 1)
				last_move += [[cord[0], cord[1] + 1]]
		else:
			self.move_down()

	def force_down(self) -> None:
		global peice_pos
		if peice_pos[0] < 70:
			lock.acquire()
			peice_pos[0] += 6
			lock.release()
			self.move_down()


	def super_rotation(self):
		global last_move
		global peice_pos

		"""
		strategy: For our 3 wide blocks. When we want to rotate draw an imaginary 3x3 box around
		the blocks center. The blocks center is 0,0. We convert all of the blocks cords
		to a 0 or 1, for X and Y (Think rotation matrix)
		
		Then rotate. After rotate translate cords back into Tetris grid


		# The stipulation, can only rotate block from a center point
		# Possible to do with I block, but difficult because its of length 4

		"""	
		# Can not rotate, if to high. Stops out of bound errors
		if peice_pos[0] < 7:
			return None

		if peice_pos[1] == 0:
			self.move_right()
			self.move_right()

		# If on the right wall and rot out of grid, kick left -2
		elif peice_pos[1] == 9:
			self.move_left()
			self.move_left()

		tmp = last_move.copy()
		self.remove_peice()
		current_row = tmp[0][0]
		current_col = tmp[0][1]
		for cord in tmp:
			y_val_temp = cord[0]
			
			cord[0] =  cord[0] - current_row
			
			# Need to adjust our values, from grid to rotation matrix
			if cord[0] > 0:
				cord[0] = 1
			elif cord[0] < 0: 
				cord[0]  = -1
			
			# Convert cord, to a [1,0] [0,0] [1,1] etc..
			# To do a rotation
			cord = [(current_row - y_val_temp) + (-2*(-cord[0])) , cord[1] - current_col]

			# Rotate around 0,0 axis (Center of block is 0,0)
			# Our cords are (y, x) -> (-x, y)
			cord[0], cord[1] = -cord[1] , cord[0]

			# Translate values back to our Tetris grid
			cord[0], cord[1] = (cord[0] * -3) + current_row , cord[1] + current_col

			self.fill_cell(cord[0], cord[1])

			last_move += [[cord[0], cord[1]]]
		
		self.show_grid()


	

class peice_T_block(peice):
	def __init__(self):
		peice.__init__(self)
	
	def create_and_place(self):
		global last_move
		global peice_pos

		self.tmp = peice_pos.copy()
		
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]
		self.fill_cell(self.tmp[0] - 3, self.tmp[1])
		last_move += [[self.tmp[0] - 3,self.tmp[1]]]
		self.fill_cell(self.tmp[0],self.tmp[1] - 1 )
		last_move += [[self.tmp[0],self.tmp[1] - 1]]
		self.fill_cell(self.tmp[0], self.tmp[1] - 1)
		last_move += [[self.tmp[0],self.tmp[1] + 1]]
		self.show_grid()


class peice_L_block(peice):
	def __init__(self):
		peice.__init__(self)
	
	def create_and_place(self):
		global last_move
		global peice_pos
		
		self.tmp = peice_pos.copy()
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]

		self.fill_cell(self.tmp[0], self.tmp[1] - 1)
		last_move += [[self.tmp[0],self.tmp[1] - 1]]

		self.fill_cell(self.tmp[0], self.tmp[1] + 1)
		last_move += [[self.tmp[0],self.tmp[1] + 1]]
		
		self.fill_cell(self.tmp[0] - 3, self.tmp[1] + 1)
		last_move += [[self.tmp[0] - 3,self.tmp[1] + 1]]
		self.show_grid()

class peice_J_block(peice):
	def __init__(self):
		peice.__init__(self)
		
	def create_and_place(self):
		global last_move
		global peice_pos
		
		self.tmp = peice_pos.copy()
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]

		self.fill_cell(self.tmp[0], self.tmp[1] - 1)
		last_move += [[self.tmp[0],self.tmp[1] - 1]]

		self.fill_cell(self.tmp[0], self.tmp[1] + 1)
		last_move += [[self.tmp[0],self.tmp[1] + 1]]
		
		self.fill_cell(self.tmp[0] - 3, self.tmp[1] - 1)
		last_move += [[self.tmp[0] - 3,self.tmp[1] - 1]]
		self.show_grid()

class peice_S_block(peice):
	def __init__(self):
		peice.__init__(self)
	
	def create_and_place(self):
		global last_move
		global peice_pos
		
		self.tmp = peice_pos.copy()
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]

		self.fill_cell(self.tmp[0], self.tmp[1] - 1)
		last_move += [[self.tmp[0],self.tmp[1] - 1]]

		self.fill_cell(self.tmp[0] - 3 , self.tmp[1])
		last_move += [[self.tmp[0] - 3,self.tmp[1]]]
		
		self.fill_cell(self.tmp[0] - 3, self.tmp[1] + 1)
		last_move += [[self.tmp[0] - 3,self.tmp[1] + 1]]
		self.show_grid()


class peice_Z_block(peice):
	def __init__(self):
		peice.__init__(self)
	
	def create_and_place(self):
		global last_move
		global peice_pos
		
		self.tmp = peice_pos.copy()
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]

		self.fill_cell(self.tmp[0], self.tmp[1] + 1)
		last_move += [[self.tmp[0],self.tmp[1] + 1]]

		self.fill_cell(self.tmp[0] - 3 , self.tmp[1])
		last_move += [[self.tmp[0] - 3,self.tmp[1]]]
		
		self.fill_cell(self.tmp[0] - 3, self.tmp[1] - 1)
		last_move += [[self.tmp[0] - 3,self.tmp[1] - 1]]
		self.show_grid()

class peice_I_block(peice):
	def __init__(self):
		peice.__init__(self)
		self.length = 4
		# There will be 3 orenations, that we need to keep track of for our rotation function
		self.rotation_count = 0 

	def create_and_place(self):
		global last_move
		global peice_pos
		global grid
		
		#peice_pos = [25, 4]
		#peice_pos = [34, 4]
		self.tmp = peice_pos.copy()

		self.fill_cell(self.tmp[0], self.tmp[1] - 1)
		last_move += [[self.tmp[0],self.tmp[1] - 1]]
		self.fill_cell(self.tmp[0], self.tmp[1])
		last_move += [[self.tmp[0],self.tmp[1]]]
		self.fill_cell(self.tmp[0], self.tmp[1] + 1)
		last_move += [[self.tmp[0],self.tmp[1] + 1]]
		self.fill_cell(self.tmp[0], self.tmp[1] + 2)
		last_move += [[self.tmp[0],self.tmp[1] + 2]]
		self.show_grid()

	
	
		

	def super_rotation(self):
		global last_move
		global peice_pos
		# Rember this requires the I block to start sideways
		if self.rotation_count == 1 or self.rotation_count == 3:
			for cord in last_move:
				if cord[1] + 2 > 9:
					self.move_left()
					self.move_left()
					break
				elif cord[1] - 2 < 0:
					self.move_right()
					self.move_right()
					break

		tmp = last_move.copy()
		y1, y2 = last_move[1][0], last_move[2][0]
		x1, x2 = last_move[1][1], last_move[2][1]
		self.remove_peice()
		if self.rotation_count == 0 or self.rotation_count == 2:
			y_level = (y1 - 1) // 3
			x_mid = (x1 + x2) / 2
			if self.rotation_count == 0:
				y_mid = y_level - .5
			elif self.rotation_count == 2:
				y_mid = y_level + .5

			y = y_mid - y_level
			
			for cord in tmp:
				# Translate to 4x4
				cord = [y, cord[1] - x_mid]
				# Swap
				cord[0], cord[1] = -cord[1], cord[0]
				# Translate back
				cord = [int(((cord[0] + y_mid) * 3) + 1), int(cord[1] + x_mid)]

				self.fill_cell(cord[0], cord[1])

				last_move += [cord]

			self.show_grid()
			self.rotation_count += 1

		else:
			
			y_mid = (((y1 - 1) / 3) + ((y2 - 1) / 3)) / 2
			
			if self.rotation_count == 1:
				x_mid = x1  + .5
				y_translate_back = y_mid - 1
				self.rotation_count += 1
			
			elif self.rotation_count == 3:
				# Reset our rotation count
				self.rotation_count = 0
				x_mid = x1  - .5
				y_translate_back = y_mid + 1

			for cord in tmp:
				cord = [y_mid - ((cord[0] - 1) / 3), cord[1] - x_mid]
				# Swap
				cord[0], cord[1] = -cord[1], cord[0]
				# Translate back
				cord = [int(((cord[0] + y_translate_back) * 3) + 1), int(cord[1] + x_mid)]

				self.fill_cell(cord[0], cord[1])

				last_move += [cord]


			self.show_grid()








class peice_O_block(peice):
	def __init__(self):
		peice.__init__(self)
		self.length = 2

	def create_and_place(self):
		global last_move
		global peice_pos
		global grid
		self.tmp = peice_pos.copy()
		for cell in range(self.length):
			self.fill_cell(self.tmp[0], self.tmp[1])
			self.fill_cell(self.tmp[0] + 3, self.tmp[1])
			last_move += [[self.tmp[0],self.tmp[1]]]
			last_move += [[self.tmp[0] + 3,self.tmp[1]]]
		
			self.tmp[1] += 1

		self.show_grid()

	def super_rotation(self) -> None:
		return None



def game_play_manual_test() -> None:
	global peice_pos
	global grid
	global peice_alive
	global count
	global user_input
	global game_alive
	global max_game_count
	global taken_cell
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	peice_control = peice()

	for i in range(30):
		if peice_control.check_grid():
			# The object must be in inner loop, instantiate new objects
			obj_peice_array = [peice_J_block(),peice_L_block(), peice_O_block(), peice_T_block(), peice_I_block(), peice_Z_block(), peice_S_block()]
			#obj_peice_array = [peice_I_block()]
			chosen_peice = obj_peice_array[random.randint(0 , len(obj_peice_array) - 1)]
			#chosen_peice = obj_peice_array[1]
			#chosen_peice = peice_O_block()
			#i_block = peice_I_block()  # When the bottom loop breaks, Our object is called once more
			chosen_peice.create_and_place()
			peice_alive = 1
			while peice_alive and game_alive and count != max_game_count:
				match user_input:
					case '':
						user_input = ''
						peice_control.move_down()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 'a':
						user_input = ''
						peice_control.move_left()
						spawn_grid.show_grid()
					case 's':
						user_input = ''
						peice_control.force_down()
						spawn_grid.show_grid()
					
					case 'd':
						user_input = ''
						peice_control.move_right()
						spawn_grid.show_grid()
					case 'q':
						user_input = ''
						chosen_peice.super_rotation()
						spawn_grid.show_grid()
						
					case 'e':
						user_input = ''
						chosen_peice.super_rotation()
						spawn_grid.show_grid()
					case 'z':
						return None

			# want to close out the unused objects
			del obj_peice_array
			

def counter_func() -> None:
	global peice_pos
	global next_cells
	global grid
	global last_move
	global count
	global game_alive 
	global max_game_count
	global taken_cell
	#grid[5][1] = "dfdsafdsa" We can reach the global grid from this functions
	for i in range(max_game_count):
		if game_alive and user_input != 'z':
			time.sleep(.25)
			#peice_pos = [49, 0]
			lock.acquire()
			peice_pos[0] += 3
			lock.release()
			count += 1			
		else:
			return None 


"""
Notes: 4/9/2024
We need to change the oder of operations for check pos. 
Currently were movind down, then checking the pos.


But we first need to check the next pos, then move. This is what is creating our dupe block error on collision

"""



def player_input_windows():
	global user_input
	global count
	global game_alive
	global max_game_count

	while count != max_game_count and game_alive:
		user_input = chr(msvcrt.getch()[0])
		user_input = ''
	os._exit()

def player_input_mac(key) -> None:
	global user_input
	global count
	global game_alive
	global max_game_count
	try:
		user_input = format(key.char)
	except AttributeError:
		user_input = ''


	if (user_input == 'z'):
		os._exit(1)
		return None
		
  
def main() -> None:
	#t1 = threading.Thread(target=game_play_manual)
	t1 = threading.Thread(target=game_play_manual_test)
	#t1 = threading.Thread(target=game_play_auto)
	t2 = threading.Thread(target=counter_func)
	#t3 = threading.Thread(target=player_input_windows)
	t3 = keyboard.Listener(on_press=player_input_mac)
	


	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()
	os._exit()

	

if __name__ == "__main__":
	main()
