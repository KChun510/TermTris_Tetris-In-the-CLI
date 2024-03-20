from pynput.keyboard import Key, Listener
import os


"""
Notes:

For constant keybored input.
On mac raw_input, should work
On windows "import  msvcrt"

"""
class grid:
	def __init__(self, length, width):
		self.length = length
		self.width = width
		self.empty = '   '
		self.fill = u"\u2588\u2588\u2588"
		self.grid = []
		self.player_pos = [0,0] # y, x

		box = ["*---* ", f"|{self.empty}| ", "*---* "]
		for row in range(self.length):
			for box_line in box:
				self.grid += [[box_line] * self.width]

		self.length = len(self.grid) - 1 


	
	def show_grid(self):
		os.system('cls||clear')
		for row in self.grid:
			print(row)

	def fill_grid(self):
		"""
		For each rows fill box, it starts at index 1, then + 3 for each proceding
		"""
		center = (self.length - 1) // 2
		self.grid[1][center] = f"|{self.fill}| "

	def place_center(self):
		"""
		For moving in the Y pos, its +/- 3, starting at 1
		For moving in the x pos, its +/- 1

		"""
		center = [(self.length // 2), (self.width // 2)]
		self.player_pos = center
		self.grid[self.player_pos[0]][self.player_pos[1]] = f"|{self.fill}| "

	def place_peice(self):
		self.grid[self.player_pos[0]][self.player_pos[1]] = f"|{self.fill}| "

	def remove_peice(self):
		self.grid[self.player_pos[0]][self.player_pos[1]] = f"|{self.empty}| "

	
	def move_pos_y(self):
		if (self.player_pos[0] >= 3 and self.player_pos[0] <= self.length - 1):
			self.remove_peice()
			self.player_pos[0] -= 3
			self.place_peice()
	
	def move_neg_y(self):
		if (self.player_pos[0] >= 0 and self.player_pos[0] < self.length - 1):
			self.remove_peice()
			self.player_pos[0] += 3
			self.place_peice()

	def move_pos_x(self):
		if (self.player_pos[1] >= 0 and self.player_pos[1] < self.width - 1):
			self.remove_peice()
			self.player_pos[1] += 1
			self.place_peice()
	
	def move_neg_x(self):
		if (self.player_pos[1] > 0 and self.player_pos[1] <= self.width - 1):
			self.remove_peice()
			self.player_pos[1] -= 1
			self.place_peice()
	
	"""
	def move_peice(self):
		#user_move = input("Input WASD: ")
		event = None
		with keyboard.Events() as events:
			event = events.get(1e6)
			event = str(event.key).strip("'")
			
			
			match event:
				case 'w':
					if (self.player_pos[0] > 4 and self.player_pos[0] < self.length):
						self.remove_peice()
						self.player_pos[0] -= 3
						self.place_peice()
				case 'a':
					if (self.player_pos[1] > 0 and self.player_pos[1] < self.width):
						self.remove_peice()
						self.player_pos[1] -= 1
						self.place_peice()
	
				case 's':
					if (self.player_pos[0] > 4 and self.player_pos[0] < self.length):
						self.remove_peice()
						self.player_pos[0] += 3
						self.place_peice()
						
				case 'd':
					if (self.player_pos[1] > 0 and self.player_pos[1] < self.width):
						self.remove_peice()
						self.player_pos[1] += 1
						self.place_peice()
						
				case 'q':
					return None



		"""





player1 = grid(5,5)
player1.place_center()
player1.show_grid()


def on_press(key):
    print('{0} pressed'.format(key))
    print(type(format(key)))
    print(format(key))
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




def main() -> None:
	with Listener(on_press=on_press) as listener:
		listener.join()





if __name__ == "__main__":
	main()









