#from pynput.keyboard import Key, Listener (MAC)
import msvcrt # Windows
import os
import time
import threading
import random
import grid_peice_obj



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

		self.show_grid()
		time.sleep(5)
		

	
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


def game_play_auto():
	global peice_pos
	global grid
	global peice_alive
	global count
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	spawn_grid.show_grid()
	peice_control = peice()	

	

	for i in range(20):
		i_block = peice_I_block()  # When the bottom loop breaks, Our object is called once more
		print( "A new object being created!!!")
		peice_alive = 1
		while peice_alive and count != 100:
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





def game_play_manual():
	global peice_pos
	global grid
	global peice_alive
	global count
	global user_input
	spawn_grid = grid_field()
	spawn_grid.show_grid()
	spawn_grid.show_grid()
	peice_control = peice()



	print(len(grid))
	time.sleep(5)	

	

	for i in range(20):
		i_block = peice_I_block()  # When the bottom loop breaks, Our object is called once more
		print( "A new object being created!!!")
		peice_alive = 1
		while peice_alive and count != 100:
			time.sleep(.25)
			match user_input:
				case '':
					user_input = ''
					peice_control.check_pos()
					peice_control.move_down()
					spawn_grid.show_grid()
				case 'q':
					user_input = ''
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
	#grid[5][1] = "dfdsafdsa" We can reach the global grid from this functions
	for i in range(100):
		print(peice_pos)
		time.sleep(.5)
		lock.acquire()
		peice_pos[0] += 3
		count += 1
		lock.release()

"""
Notes: 4/9/2024
We need to change the oder of operations for check pos. 
Currently were movind down, then checking the pos.


But we first need to check the next pos, then move. This is what is creating our dupe block error on collision

"""



"""

T0 build our top bound function. (Stopping game when run out of space at top)
We need to extend our grid by 2 spaces in the Y. We will not show these extra two on the grid

https://www.youtube.com/watch?v=-FAzHyXZPm0 
Blocks of 4 + tall, start off as 2 height for the first few frames. Then Plus 1 to height proceeding frames.
The L and I peice

"""



def player_input():
	global user_input
	global count

	while count != 100:
		user_input = chr(msvcrt.getch()[0])





def main() -> None:
	t1 = threading.Thread(target=game_play_manual)
	#t1 = threading.Thread(target=game_play_auto)
	t2 = threading.Thread(target=counter_func)
	t3 = threading.Thread(target=player_input)

	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()

if __name__ == "__main__":
	main()




"""
cd onedrive/desktop/termtres/windows_copy

"""




