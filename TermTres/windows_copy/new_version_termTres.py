from pynput.keyboard import Key, Listener
import os
import time
import threading
import random




peice_pos = [0,0]
lock = threading.Lock()
grid = []
last_move = []  # We will keep a tempory trace of the index's are filled. Needed for peice deletion
next_cells = []
time_count = 0


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
		peice_pos = [13 , 5]
		print(f"This is from the peice contrustor {peice_pos}")


	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		peice_pos = self.center
		grid[peice_pos[0]][peice_pos[1]] = f"|{self.fill}| "
	

	def check_block_top(self) -> bool:
		if (grid[peice_pos[0] - 3][peice_pos[1]] == f"|{self.fill}| "):
			return True
		else:
			return False


	def check_block_left(self) -> bool:
		if (grid[peice_pos[0]][peice_pos[1] - 1] == f"|{self.fill}| "):
			return True
		else:
			return False	

	def check_block_right(self) -> bool:
		if (grid[peice_pos[0]][peice_pos[1] + 1] == f"|{self.fill}| "):
			return True
		else:
			return False


	def check_block_under(self) -> bool:
		print(grid[peice_pos[0] + 3][peice_pos[1]])
		print(type(grid[peice_pos[0] + 3][peice_pos[1]]))
		print(type(f"|{self.fill}| ")) 
		time.sleep(2)
		if (grid[peice_pos[0] + 3][peice_pos[1]] == f"|{self.fill}| "):
			return True
		else:
			return False

	def fill_cell(self, y: int, x:int):
		grid[y][x] = f"|{self.fill}| "

	def remove_peice(self) -> None:
		global last_move
		global grid
		tmp = last_move.copy()
		last_move = []
		for cords in tmp:
			grid[cords[0]][cords[1]]  = f"|{self.empty}| "

# Can add extra logic here to account for set blocks on the bottom
	def move_down(self) -> None: # Moves our block down one space at a time
		global peice_pos
		global last_move
		global next_cells

		print(f"Printing from move down \nThis the center val :{peice_pos}\nThis is the last_move: {last_move}\nThis is the value of next: {next_cells}")
	

		self.remove_peice()
		print(next_cells)
		last_move = []
		for cord in next_cells:
			print(cord)
			self.fill_cell(cord[0], cord[1])
			last_move += [[cord[0], cord[1]]]
		next_cells = []
		

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

class peice_I_block(peice):
	def __init__(self):
		peice.__init__(self)
		global last_move
		global peice_pos
		global grid
		global next_cells
		"""
		lock.acquire()
		#peice_pos = self.center
		lock.release()
		"""
		self.length = 4


		last_move = [] # We will keep a tempory trace of the index's are filled. Needed for peice deletion
		#print(peice_pos)
		# peice_pos[0] += 3
		
		self.tmp = peice_pos.copy()

		print(self.tmp)
		
		for cell in range(self.length):
			grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
			last_move += [[self.tmp[0],self.tmp[1]]]
			#next_cells += [[self.tmp[0] + 3,self.tmp[1]]]
			
			self.tmp[0] += 3
		print(f"The first appendage: \nlast: {last_move}\nnext: {next_cells}")
		

	
	def rotate_block_left(self):
		global peice_pos
		global last_move
		global next_cells
		# This is in form of y, x

		lock.acquire()
		
		self.tmp = peice_pos.copy()
		lock.release()

		self.remove_peice()
		print("Rotate Left")
		print(f"tmp the center pos {self.tmp}")
		print(f"The real position {peice_pos}")
		time.sleep(.3)
		# IF there is a block underneath our start block and there is enough space on the left side
		if(self.check_block_under() and peice_pos[1] >= 3):
			for cell in range(self.length):
				print(f"Under went a check !!!")
				print(f"There is a block underneath")
				time.sleep(1)
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				last_move += [[self.tmp[0],self.tmp[1]]] 
				
				
				self.tmp[1] -= 1

		
			self.tmp = peice_pos.copy()
		
		
		# IF there is a block to the left our start block and enough space up top
		elif(self.check_block_left() and peice_pos[0] >= 10):			
			for cell in range(self.length):
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				last_move += [[self.tmp[0],self.tmp[1]]]
				
					
				self.tmp[0] -= 3
				

			self.tmp = peice_pos.copy()
			

		# if there is a block up top, and enough space to the right
		elif(self.check_block_top() and peice_pos[1] <= 7):
			
			
			for cell in range(self.length):
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				last_move += [[self.tmp[0],self.tmp[1]]]
				
				self.tmp[1] += 1
			
			
			self.tmp = peice_pos.copy()
	

		# if there is a block to the right and enough space bellow
		elif(self.check_block_right() and peice_pos[0] <= 48):
			for cell in range(self.length):
			
				grid[self.tmp[0]][self.tmp[1]] = f"|{self.fill}| "
				
				last_move += [[self.tmp[0],self.tmp[1]]]
				self.tmp[0] += 3
			
		
			self.tmp = peice_pos.copy()
		

		else:
			print("Invalid Move")
			time.sleep(5)


def counter_func():
	global peice_pos
	global next_cells
	global grid
	global last_move
	global time_count
	#grid[5][1] = "dfdsafdsa" We can reach the global grid from this functions
	for i in range(20):
		lock.acquire()
		time.sleep(1)
		peice_pos[0] =  peice_pos[0]
		time_count += 1
		lock.release()

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
			#case "e":
			#	i_block.rotate_block_right()
			#	spawn_grid.show_grid()
			


def game_play():
	global peice_pos
	global time_count
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	i_block = peice_I_block()
	spawn_grid.show_grid()
	peice_control = peice()

	while time_count < 20:
		input_for_control = random.randint(1, 1)
		match input_for_control:
			case 0:
				peice_control.move_down()
				spawn_grid.show_grid()
			case 1:
				i_block.rotate_block_left()
				spawn_grid.show_grid()
			case 2:
				
				i_block.rotate_block_right()
				spawn_grid.show_grid()


def main() -> None:
	#t1 = threading.Thread(target=game_play)
	t1 = threading.Thread(target=game_play_manual)
	#t2 = threading.Thread(target=counter_func)


	t1.start()
	#t2.start()

	t1.join()
	t2.join()
	

if __name__ == "__main__":
	main()


