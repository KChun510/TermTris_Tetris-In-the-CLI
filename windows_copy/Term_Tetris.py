from pynput.keyboard import Key, Listener
import os
import time
import threading
import random



"""
Notes:

For constant keybored input.
On mac raw_input, should work
On windows "import  msvcrt"

"""
"""


Task:
split the decrement function into its own thread. 
And pass vars between them (The Threads)
LOOK at file threading_var.py

cd onedrive/desktop/termtres/windows_copy
python3 Term_Tetris.py

"""


peice_pos = [0,0]
lock = threading.Lock()
grid = []
last_move = []  # We will keep a tempory trace of the index's are filled. Needed for peice deletion
taken_cell = []
peice_alive = 1



class grid_field:
	def __init__(self):
		global grid
		self.length = 20
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
		for row in grid:
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
			if cord in taken_cell:
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

			collision_flag_block = 1

		if len(last_move) > 0:
			for cord in tmp: 
				if (cord[0] >= 58):
					collision_flag_floor = 1
					break
			
		if collision_flag_floor == 1 and collision_flag_block == 1:
			for cord in tmp:
				self.fill_cell(cord[0] - 3 , cord[1])
				taken_cell += [[cord[0] - 3, cord[1]]]
		
			self.show_grid()
		
			lock.acquire()
			last_move = []
			peice_pos = [1, 5]
			peice_alive = 0
			lock.release()

			return False

		

		elif collision_flag_floor == 1:
			self.remove_peice()
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
				self.fill_cell(cord[0] - 3 , cord[1])
				taken_cell += [[cord[0] - 3, cord[1]]]
		
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


		# This is how we sink the data between threads.
		# Make up for the incrimented value in our counter func
		# Only move down if value was updated

		if len(last_move) > 0 and last_move[0][0] < 58:
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



"""
Moving forward we are going to use a sinlgle block to track position and movement
Think of the center peice/when we were only moving around a single block

"""





class peice_I_block(peice):
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
		print(self.tmp)


		
		for cell in range(self.length):
			grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
		
			last_move += [[self.tmp[0],self.tmp[1]]]
			#next_cells += [[self.tmp[0] + 3,self.tmp[1]]]
		
			self.tmp[0] += 3

		time.sleep(.2) 
		

	
	def rotate_block_left(self):
		global peice_pos
		global last_move
		global next_cells
		# This is in form of y, x


		print("Turn Left")
		self.tmp = peice_pos.copy()
		next_cells = []
		# IF there is a block underneath our start block and there is enough space on the left side
		if(self.check_pos()):
			if(peice_pos[1] >= 3 and peice_pos[0] <= 48 and self.check_block_under()):
			
				self.remove_peice()

				
				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]] 
					
					self.tmp[1] -= 1

				self.tmp = peice_pos.copy()
			
			
			# IF there is a block to the left our start block and enough space up top
			elif(peice_pos[0] >= 10 and self.check_block_left()):
				self.remove_peice()

				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]
						
					self.tmp[0] -= 3
					


				self.tmp = peice_pos.copy()
				

			# if there is a block up top, and enough space to the right
			elif(peice_pos[1] <= 7 and self.check_block_top()):
				
				self.remove_peice()

				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]

					self.tmp[1] += 1
				


				self.tmp = peice_pos.copy()
		

			# if there is a block to the right and enough space bellow
			elif(peice_pos[0] <= 48 and self.check_block_right()):

				self.remove_peice()
				

				for cell in range(self.length):
				
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					
					last_move += [[self.tmp[0],self.tmp[1]]]
					self.tmp[0] += 3
			
				self.tmp = peice_pos.copy()
			

		else:
			print("Invalid Move!!!!!!")
			self.move_down()



		# IF there is a block ontop of the start and enough space to the right


		# IF there is a block to the right of start and enough space on the bottom


	def rotate_block_right(self):
		global peice_pos
		global last_move
		global next_cells
		lock.acquire()
		self.tmp = peice_pos.copy()
		next_cells = []
		lock.release()

		self.remove_peice()
		time.sleep(.1)
		# if there is a block bellow our start block, and enough space to the right
		if(self.check_block_under() and peice_pos[1] <= 7):
			self.remove_peice()
			for cell in range(self.length):
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "


				last_move += [[self.tmp[0],self.tmp[1]]]

				self.tmp[1] += 1

			lock.acquire()
			self.tmp = peice_pos.copy()
			lock.release()
		
		# if there is a block to the right, and enough space up top
		elif(self.check_block_right() and peice_pos[0] >= 10):
			self.remove_peice()
			print(f"This is the value of pos: {peice_pos} value of: {self.tmp}")
			for cell in range(self.length):
				
			
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				
				last_move += [[self.tmp[0],self.tmp[1]]]
				self.tmp[0] -= 3
			
			lock.acquire()
			self.tmp = peice_pos.copy()
			lock.release()		

		# if there is a block up top, and enough space to the left
		elif(self.check_block_top() and peice_pos[1] >= 3):
			
			self.remove_peice()

			for cell in range(self.length):

				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "

				last_move += [[self.tmp[0],self.tmp[1]]]

				self.tmp[1] -= 1
			
			lock.acquire()
			self.tmp = peice_pos.copy()
			lock.release()

			

		# if there is a block to the left, and enough space on the bottom
		elif(self.check_block_left() and peice_pos[0] <= 48):

			self.remove_peice()
			
			for cell in range(self.length):
			
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				
				last_move += [[self.tmp[0],self.tmp[1]]]
				self.tmp[0] += 3
			
			lock.acquire()
			self.tmp = peice_pos.copy()
			lock.release()
		else: 
			print("Invalid Move")
		


	def place_peice(self):
		center = self.center
		grid[self.center[0]][self.center[1]] = f"|{self.fill}| "



"""
def on_press(key):
    if key == Key.esc:
        # Stop listener
        return False
    else:
    	key = str(key).strip("'")
    	match key:
    		case "w":
    			peice1.move_pos_y()
    			peice1.show_grid()
    		case "a":
    			peice1.move_neg_x()
    			peice1.show_grid()
    		case "s":
    			peice1.move_neg_y()
    			peice1.show_grid()
    		case "d":	
    			peice1.move_pos_x()
    			peice1.show_grid()
    		case "q":
    			return None


"""

"""
def on_press(key):
    if key == Key.esc:
        # Stop listener
        return False
    else:
    	key = str(key).strip("'")
    	match key:
    		case "w":
    			player1.move_pos_y()
    			player1.show_grid()
    		case "a":
    			player1.move_neg_x()
    			player1.show_grid()
    		case "s":
    			player1.move_neg_y()
    			player1.show_grid()
    		case "d":	
    			player1.move_pos_x()
    			player1.show_grid()
    		case "q":
    			return None
"""

# Collect events until released

def game_play_manual():
	global peice_pos
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	i_block = peice_I_block()
	spawn_grid.show_grid()
	

	move = ""
	while move != "z":
		move = input("Enter what you want to do: ")
		match move:
			case "q":
				i_block.rotate_block_left()
				spawn_grid.show_grid()
			case "s":
				i_block.move_down()
				spawn_grid.show_grid()
			case "e":
				i_block.rotate_block_right()
				spawn_grid.show_grid()


def game_play():
	global peice_pos
	global grid
	global peice_alive
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	spawn_grid.show_grid()
	peice_control = peice()	

	

	for i in range(20):
		i_block = peice_I_block()  # When the bottom loop breaks, Our object is called once more
		print( "A new object being created!!!")
		peice_alive = 1
		while peice_alive:
			input_for_control = random.randint(0, 1)
			time.sleep(.25)
			match input_for_control:
				case 0:
					peice_control.check_pos()
					peice_control.move_down()
					spawn_grid.show_grid()
				case 1:
					peice_control.check_pos()
					i_block.rotate_block_left()
					spawn_grid.show_grid()

				case 2:
					peice_control.move_down()
					spawn_grid.show_grid()
				case 4:
					i_block.rotate_block_right()
					spawn_grid.show_grid()


	"""
	with Listener(on_press=on_press) as listener:
		listener.join()
	"""

"""
def counter_func():
	global peice_pos
	global next_cells
	global last_move
	peice_control = peice()
	for i in range(20):
		time.sleep(.75)
		lock.acquire()
		peice_pos[0] += 3
		for i in range(len(last_move)):
			next_cells += [[last_move[i][0] + 3, last_move[i][1]]]
		lock.release()
"""


"""
Reason for current glitch. Before the block is placed. The last moved is made. Then the last moves are passed to "Removed_peiced"


"""



"""
When the counter is at 1.5, and the time between moves is 1 second. We got the best performace

"""
def counter_func():
	global peice_pos
	global next_cells
	global grid
	global last_move
	#grid[5][1] = "dfdsafdsa" We can reach the global grid from this functions
	for i in range(100):
		print(peice_pos)
		time.sleep(1)
		lock.acquire()
		peice_pos[0] += 3
		lock.release()


	


		


def main() -> None:
	t1 = threading.Thread(target=game_play)
	#t1 = threading.Thread(target=manual_game_play)
	t2 = threading.Thread(target=counter_func)


	t1.start()
	t2.start()

	t1.join()
	t2.join()
	




if __name__ == "__main__":
	main()




"""
cd onedrive/desktop/termtres/windows_copy

"""




