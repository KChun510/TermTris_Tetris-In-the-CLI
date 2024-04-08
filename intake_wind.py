import msvcrt

"""
input_char = "z"
while input_char != "q":
   input_char = msvcrt.getch()
   print(input_char)
   if input_char.upper() == 'S': 
      print ('YES')
"""


def main():
   print('Press s or n to continue:\n')
   input_char = chr(msvcrt.getch()[0])
   print(type(input_char))
   print(input_char)
   if input_char.upper() == 'S': 
      print('YES')





main()