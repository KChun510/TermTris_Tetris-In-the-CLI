import threading
import time 
import os


global_count = 0
i = 0
lock = threading.Lock()
grid = []

"""
Notes:
The idea of thread locking. Locking



"""
class test_class():
	def __init__(self):
		global global_count
		self.var = 0
		global grid

	def test_func_class(self):
		global global_count
		self.var = 0
		global grid
		global i
		while i != 10:
			print(f"from the class: {global_count}")
			print(f"The value of I: {i}")
			print(f"The values in grid: {grid}")
			time.sleep(.5)
			os.system('cls||clear')

			if i == 5:
				grid = []
		
			
			

"""
When locking a thread. It suspends, the other threads, untill release. 
In test_func(), we are locking the thread. 

When test_class().test_func_class, try's to access the global vars. It also gets suspended, until 
release in test_func()

"""
def test_func():
	global global_count
	global i
	global grid
	while i < 15:
		time.sleep(1)
		lock.acquire()
		global_count += 1
		i += 1
		grid += [i]
		lock.release()


def append_func():
	global grid
	global i
	while i < 20:
		time.sleep(1)
		lock.acquire()
		
		lock.release()
	



def main():
	t1 = threading.Thread(target=test_func)
	obj1 = test_class()
	t2 = threading.Thread(target=obj1.test_func_class)
	#t3 = threading.Thread(target=append_func)

	t1.start()
	t2.start()
	#t3.start()

	t1.join()
	t2.join()
	#t3.start()



main()