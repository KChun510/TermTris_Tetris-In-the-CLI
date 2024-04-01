import threading

class test_pass():
	def __init__(self):
		self.name = "Kyle Chun"




def testing_func(obj1):
	for i in range(10):
		print("Freak you")




def main():
	obj1 = test_pass()
	t1 = threading.Thread(target=testing_func, args=(obj1))
	t1.start()
	t1.join()


main()