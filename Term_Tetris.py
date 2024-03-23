from pynput.keyboard import Key, Listener
import os
import time


"""
Notes:

For constant keybored input.
On mac raw_input, should work
On windows "import  msvcrt"

"""






class grid:
	def __init__(self):
		self.length = 20
		self.width = 10
		self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"
		self.grid = []
		


		box = ["*---* ", f"|{self.empty}| ", "*---* "]
		for row in range(self.length):
			for box_line in box:
				self.grid += [[box_line] * self.width]

		self.length = len(self.grid) - 1 

	def show_grid(self):
		os.system('cls||clear')
		for row in self.grid:
			print(''.join(row))

	
	
class peice(grid):
	def __init__(self):
		grid.__init__(self)
		#self.grid = grid_arr
		#self.center = [(self.length // 2), (self.width // 2)]
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"
		self.peice_pos = [0,0] # y, x

	"""
	def fill_grid(self):
		# This method fills a space 
		
		#For each rows fill box, it starts at index 1, then + 3 for each proceding
		
		center = (self.length - 1) // 2
		self.grid[1][center] = f"|{self.fill}| "

	"""
	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		self.peice_pos = self.center
		self.grid[self.peice_pos[0]][self.peice_pos[1]] = f"|{self.fill}| "

	def place_peice(self):
		self.grid[self.peice_pos[0]][self.peice_pos[1]] = f"|{self.fill}| "

	def remove_peice(self):
		self.grid[self.peice_pos[0]][self.peice_pos[1]] = f"|{self.empty}| "

	
	def move_pos_y(self):
		if (self.peice_pos[0] >= 3 and self.peice_pos[0] <= self.length - 1):
			self.remove_peice()
			self.peice_pos[0] -= 3
			self.place_peice()
	
	def move_neg_y(self):
		if (self.peice_pos[0] >= 0 and self.peice_pos[0] < self.length - 1):
			self.remove_peice()
			self.peice_pos[0] += 3
			self.place_peice()

	def move_pos_x(self):
		if (self.peice_pos[1] >= 0 and self.peice_pos[1] < self.width - 1):
			self.remove_peice()
			self.peice_pos[1] += 1
			self.place_peice()
	
	def move_neg_x(self):
		if (self.peice_pos[1] > 0 and self.peice_pos[1] <= self.width - 1):
			self.remove_peice()
			self.peice_pos[1] -= 1
			self.place_peice()
"""
Moving forward we are going to use a sinlgle block to track position and movement
Think of the center peice/when we were only moving around a single block

"""





class peice_I_block(peice):
	def __init__(self):
		peice.__init__(self)
		self.length = 4
		self.peice_pos = self.center
		self.peice_pos[0] = 1
		
		self.last_move = [] # We will keep a tempory trace of the index's are filled. Needed for peice deletion
		
		# self.peice_pos[0] += 3
		tmp = self.peice_pos[0]
		
		for cell in range(self.length):
			self.grid[tmp][self.peice_pos[1]] = f"|{self.fill}| "

			self.last_move += [[tmp,self.peice_pos[1]]]
			
			tmp += 3

	def remove_peice(self):
		print(self.last_move)
		for cords in self.last_move:
			self.grid[cords[0]][cords[1]]  = f"|{self.empty}| "

		self.last_move = []




	
	def rotate_block_left(self):
		# This is in form of y, x
		self.remove_peice()
		
		tmp = self.peice_pos
		# IF there is a block underneath our start block
		#print(self.grid[self.peice_pos[0] + 3][self.peice_pos[1]] == self.grid[self.peice_pos[0]][self.peice_pos[1]])
		#print(self.grid[self.peice_pos[0]][self.peice_pos[1]- 1] == self.grid[self.peice_pos[0]][self.peice_pos[1]])
		
		# IF there is a block underneath our start block and there is enough space on the left side
		if(self.grid[self.peice_pos[0] + 3][self.peice_pos[1]] == self.grid[self.peice_pos[0]][self.peice_pos[1]] and self.peice_pos[1] >= 3):
			for cell in range(self.length):
				self.grid[self.peice_pos[0]][tmp[1]] = f"|{self.fill}| "
				
				self.last_move += [[self.peice_pos[0],tmp[1]]]
				
				tmp[1] -= 1
		
		# IF there is a block to the left our start block and enough space up top
		elif(self.grid[self.peice_pos[0]][self.peice_pos[1] - 1] == self.grid[self.peice_pos[0]][self.peice_pos[1]] and self.peice_pos[1] >= 12):
			for cell in range(self.length):
				self.grid[self.peice_pos[0]][tmp[0]] = f"|{self.fill}| "
				
				self.last_move += [[self.peice_pos[0], tmp[0]]]


				tmp[0] -= 3

		# IF there is a block ontop of the start and enough space to the right


		# IF there is a block to the right of start and enough space on the bottom


	def rotate_block_right(self):
		tmp = self.peice_pos[1]
		for cell in range(self.length):
			self.grid[self.peice_pos[0]][tmp] = f"|{self.fill}| "
			tmp += 1









	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		tmp_pos = self.peice_pos
		# The Y block
		for cell in range(self.i_block_dims[0]):
			if cell >= 1:
				tmp_pos[0] -= 3
				self.grid[tmp_pos[0]][tmp_pos[1]] = f"|{self.fill}| "
			else:
				self.grid[tmp_pos[0]][tmp_pos[1]] = f"|{self.fill}| "

		
		 # The X block
		for cell in range(self.i_block_dims[1] - 1):
			tmp_pos[1] -= 1
			self.grid[tmp_pos[0]][tmp_pos[1]] = f"|{self.fill}| "


	def place_peice(self):
		self.grid[self.peice_pos[0]][self.peice_pos[1]] = f"|{self.fill}| "

	




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


def main() -> None:	
	player1 = grid()
	player1.show_grid()
	peice1 = peice()
	#print(peice1.length)
	i_block = peice_I_block()
	i_block.show_grid()
	#i_block.place_center()
	#i_block.show_grid()
	#time.sleep(2)
	#i_block.rotate_block_left()
	#i_block.place_center()
	#i_block.show_grid()
	#i_block.place_center()
	#i_block.rotate_block_right()
	time.sleep(2)
	i_block.rotate_block_left()
	i_block.show_grid()
	#i_block.rotate_block_left()
	#i_block.show_grid()
	#i_block.place_center()

	"""
	with Listener(on_press=on_press) as listener:
		listener.join()
	"""




if __name__ == "__main__":
	main()









