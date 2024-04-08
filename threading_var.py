# Importing the threading module
import threading 
# Declraing a lock
lock = threading.Lock()
deposit = 100
# Function to add profit to the deposit
def add_profit(): 
    global deposit
    for i in range(1):
        lock.acquire()
        deposit = deposit + 1
        lock.release()
# Function to deduct money from the deposit
def pay_bill(): 
    global deposit
    for i in range(1):
        lock.acquire()
        deposit = deposit - 10
        lock.release()
# Creating threads
thread1 = threading.Thread(target = add_profit, args = ())
thread2 = threading.Thread(target = pay_bill, args = ())
# Starting the threads  
thread1.start() 
thread2.start() 
# Waiting for both the threads to finish executing 
thread1.join()
thread2.join()
# Displaying the final value of the deposit
print(deposit)