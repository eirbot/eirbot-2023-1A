"""
Program to test the use of threading in python
Covers the following topics:
    - threading
    - locks
    - shared variables
    - conditional stop
"""
import threading
import time

class Test:
    def __init__(self):
        # declare thread
        self.thread = threading.Thread(target=self.run, args=())

        # declare conditional stop for this thread
        self.stop = False

        # declare lock
        self.lock = threading.Lock()

        # declare shared variable between threads
        self.shared = 0

    def run(self):
        # this function will run in a separate thread of the class instance Test
        # while stop is not True, the thread will run
        while not self.stop:

            # wait for lock to be free
            self.lock.acquire()

            # do something with shared variable
            self.shared = self.shared + 1
            print("thread {}".format(self.shared))

            # release lock, so other threads can use the shared variable
            self.lock.release()

if __name__ == "__main__":

    # create instance of Test class
    t = Test()

    # start thread
    t.thread.start()
    begin = time.time()
    while time.time() - begin < 5:

        # wait for lock to be free
        t.lock.acquire()

        # do something with shared variable
        t.shared = t.shared + 1
        print("main {}".format(t.shared))

        # release lock, so other threads can use the shared variable
        t.lock.release()

    # stop thread
    t.stop = True