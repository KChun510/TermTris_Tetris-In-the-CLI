import threading
import time

LOCK = threading.Lock()


class Printer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Printer, self).__init__(*args, **kwargs)
        self.daemon = True
        self.i = 0

    def run(self):
        while True:
            with LOCK:
                print(self.i)
                self.i += 1
                time.sleep(1)


input('press enter to start thread\n')
Printer().start()
input('press enter to pause thread\n')
print('acquiring...')
LOCK.acquire()
print('acquired')
input('press enter to resume thread\n')
LOCK.release()
input('press enter to exit program\n')
print('bye!')
