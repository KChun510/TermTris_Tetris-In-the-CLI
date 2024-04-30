from pynput import keyboard
 #mac
#import msvcrt # Windows
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
count = 0
user_input = ""
game_alive = True
cell_taken_flag = False
cleard_row = []

max_game_count = 250



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
		for row in grid[6:]:
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
		peice_pos = [1 , 5]


	def show_grid(self):
		os.system('cls||clear')
		for row in grid[6:]:
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



	"""
	Current bug... with move left & right.


	These functions only account for the center block.
	So lets say we rotate, then move rigth. will get an index error


	"""





	
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
		print(peice_pos)
		if peice_pos[0] < 64 and not self.is_cell_taken_force():
			lock.acquire()
			peice_pos[0] += 3
			lock.release()
			self.move_down()






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
	

		for cell in range(self.length):
			grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
		
			last_move += [[self.tmp[0],self.tmp[1]]]
			#next_cells += [[self.tmp[0] + 3,self.tmp[1]]]
		
			self.tmp[0] += 3

		self.show_grid()
		

	
	def rotate_block_left(self):
		global peice_pos
		global last_move
		global next_cells
		global cardinal
		# This is in form of y, x


	
		self.tmp = peice_pos.copy()
		next_cells = []

		# IF there is a block underneath our start block and there is enough space on the left side
		if(not self.is_cell_taken_force() and self.check_pos()):
			if(peice_pos[0] <= 54 and peice_pos[1] >= 3 and self.check_block_under()):
			
				self.remove_peice()

				cardinal = 'west'
				
				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]] 
					
					self.tmp[1] -= 1

	

				self.tmp = peice_pos.copy()


			
			
			# IF there is a block to the left our start block and enough space up top
			elif(peice_pos[1] > 0 and self.check_block_left() and peice_pos[0] >= 6):
				self.remove_peice()

				cardinal = 'north'


				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]
						
					self.tmp[0] -= 3
		

				self.tmp = peice_pos.copy()
				

			# if there is a block up top, and enough space to the right
			elif(peice_pos[0] <= 54 and self.check_block_top() and peice_pos[1] <= 6 ):
				
				self.remove_peice()

				cardinal = 'east'

				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]

					self.tmp[1] += 1
			

				self.tmp = peice_pos.copy()

		

			# if there is a block to the right and enough space bellow
			elif(peice_pos[0] <= 54 and peice_pos[1] < 9 and self.check_block_right()):

				self.remove_peice()

				cardinal = 'south'
				

				for cell in range(self.length):
				
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					
					last_move += [[self.tmp[0],self.tmp[1]]]
					self.tmp[0] += 3

				self.tmp = peice_pos.copy()
			
			else:
				self.move_down()
			

		else:
			self.move_down()



		# IF there is a block ontop of the start and enough space to the right


		# IF there is a block to the right of start and enough space on the bottom


	def rotate_block_right(self):
		global peice_pos
		global last_move
		global next_cells
		global cardinal
		# This is in form of y, x

	
		
		self.tmp = peice_pos.copy()
		next_cells = []
		
		if(not self.is_cell_taken_force() and self.check_pos()):
			# if there is a block bellow our start block, and enough space to the right
			if(peice_pos[0] <= 54 and peice_pos[1] <= 6 and self.check_block_under()):
			
				self.remove_peice()
			
				cardinal = 'east'
				
		
				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]

					self.tmp[1] += 1

				self.tmp = peice_pos.copy()
	
			
			# if there is a block to the right, and enough space up top
			elif(peice_pos[0] <= 54 and peice_pos[1] < 9 and self.check_block_right()):
				self.remove_peice()
				
				
				cardinal = 'north'

				for cell in range(self.length):
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					last_move += [[self.tmp[0],self.tmp[1]]]
					self.tmp[0] -= 3
				
				self.tmp = peice_pos.copy()


			# if there is a block up top, and enough space to the left
			elif(peice_pos[0] <= 54 and peice_pos[1] >= 3 and self.check_block_top()):
				
				self.remove_peice()
			
				

				cardinal = 'west'

				for cell in range(self.length):

					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "

					last_move += [[self.tmp[0],self.tmp[1]]]

					self.tmp[1] -= 1
				
				
				self.tmp = peice_pos.copy()
				

			# if there is a block to the left, and enough space on the bottom
			elif(peice_pos[0] <= 54 and self.check_block_left()):

				self.remove_peice()
				
				cardinal = 'south'
				
				for cell in range(self.length):
				
					grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
					
					last_move += [[self.tmp[0],self.tmp[1]]]
					self.tmp[0] += 3
				
				self.tmp = peice_pos.copy()


			else:
				self.move_down()


		else: 
			self.move_down()
	


	def place_peice(self):
		grid[self.center[0]][self.center[1]] = f"|{self.fill}| "


def game_play_auto():
	global peice_pos
	global grid
	global peice_alive
	global count
	global max_game_count
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	spawn_grid.show_grid()
	peice_control = peice()	

	

	for i in range(20):
		if peice_control.check_grid():
			i_block = forceice_I_block()  # When the bottom loop breaks, Our object is called once more
			peice_alive = 1
			while peice_alive and count != max_game_count:
				input_for_control = random.randint(0, 5)
				match input_for_control:
					case 0:
						peice_control.movge_down()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 1:
						i_block.rotate_block_left()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 2:
						i_block.rotate_block_right()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 3:
						
						peice_control.force_down()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 4:
						
						peice_control.move_left()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 5:
						
						peice_control.move_right()
						spawn_grid.show_grid()
						time.sleep(.15)



"""

Important notes: 
The player pos is in the form of y,x

There are 66 rows. Every 3 rows is where the the "Empty/fill" cells are located
"""






def game_play_manual():
	global peice_pos
	global grid
	global peice_alive
	global count
	global user_input
	global game_alive
	global max_game_count
	global taken_cell
	global cleard_row
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	spawn_grid.show_grid()
	peice_control = peice()	

	

	for i in range(30):
		if peice_control.check_grid():
			i_block = peice_I_block()  # When the bottom loop breaks, Our object is called once more
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
						time.sleep(.15)
					case 's':
						user_input = ''
						peice_control.force_down()
						spawn_grid.show_grid()
					
					case 'd':
						user_input = ''
						peice_control.move_right()
						spawn_grid.show_grid()
						time.sleep(.15)
					case 'q':
						user_input = ''
						i_block.rotate_block_left()
						spawn_grid.show_grid()
						
					case 'e':
						user_input = ''
						i_block.rotate_block_right()
						spawn_grid.show_grid()
					
				
					



"""
def counter_func():
	global peice_pos
	global next_cells
	global last_move
	peice_control = peice()
	for i in range(20):
		time.sleep(.65)
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
cd onedrive/desktop/termtres/windows_copy
python3 Term_Tetris.py

"""


"""
When the counter is at 1.5, and the time between moves is 1 second. We got the best performace

"""
def counter_func():
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
		if game_alive:
			
			time.sleep(.25)
			
			#peice_pos = [49, 0]
		
			lock.acquire()
			peice_pos[0] += 3
			lock.release()

			
			count += 1
			
			
		else:
			break


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


def player_input_mac(key):
	global user_input
	global count
	global game_alive
	global max_game_count

	user_input = format(key.char)
   




def main() -> None:
	t1 = threading.Thread(target=game_play_manual)
	#t1 = threading.Thread(target=game_play_auto)
	t2 = threading.Thread(target=counter_func)
	#t3 = threading.Thread(target=player_input)
	t3 = keyboard.Listener(on_press=player_input_mac)
	


	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()

	

if __name__ == "__main__":
	main()