





class MyClass():
	def __init__(self):
		self.name = 'Kyle Chun'




	def test_func(self):
		print("Wut the fuck is this place")

	def test_func2(self):
		print("Wut the fuck is this place")






def main():
	#obj = MyClass()

	obj_array = [MyClass()]
	try:
		getattr(obj_array[0], 'test_func2')()
	except:
		print("No obj found")



if __name__ == '__main__':
	main()
