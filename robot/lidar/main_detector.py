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
import sys
import os
import asyncio

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar
from rplidar import *
import lidar
import basic_detector

DMAX = 1000
IMIN = 0
IMAX = 200

fig = plt.figure()
ax = plt.subplot(111, projection='polar')
line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
ax.set_rmax(DMAX)
ax.grid(True)
ax.axis('off')
#add a red dot at the center of the lidar with polar coordinates (0,0)
ax.add_patch(plt.Circle((0, 0), 10, color='r', fill=True))

class LidarScan:
    def __init__(self):
        # declare thread
        self.stop = False
        self.thread = threading.Thread(target=self.get_lidar_img, args=())

        # declare conditional stop for this thread
        self.lidar_obj, self.iterator = lidar.init_lidar()

        # declare lock
        self.lock = threading.Lock()
        # declare shared variable between threads
        self.offsets = None
        self.intens = None
        self.shared_offset = None
        self.shared_intens = None

    def round_time(self, t):
        # round value to 0 if it is less than 0.5, otherwise round to 1
        return int(t + 0.5)

    def round_decimal(self,t):
        # round to 1 decimal place
        return round(t, 1)

    def round_under(self, t):
        # round everything to the lower integer
        return int(t)

    def get_lidar_img(self):
        begin = time.time()
        while time.time() - begin < 60:
            begin_2 = time.time()
            self.intens, self.offsets =lidar.get_scan_var(self.iterator)
            #print(time.time()-self.round_under(time.time()))
            #print('test',(self.round_decimal(time.time()-self.round_under(time.time())))*10)
            #if (self.round_decimal(time.time()-self.round_under(time.time()))*10)%1== 0:
            self.shared_offset = self.offsets
            self.shared_intens = self.intens
            #print('time',time.time()-begin_2)

            
        lidar.stop_lidar(self.lidar_obj)

    
    def main_thread(self):
        i=0
        strategy_command_list = ["motor:0.00:0.00:1.57", "led:1.00:0.00:0.00", "motor:0.00:0.00:1.57", "led:1.00:0.00:0.00"]
        
        scanner.thread.start()
        begin = time.time()
        offsets = None
        intens = None
        while time.time() - begin < 110:
            time.sleep(0.05)
            offsets = self.shared_offset
            intens = self.shared_intens
            if offsets is not None:
                line.set_offsets(offsets)
                line.set_array(intens)
                absolute_path = os.path.abspath(os.path.dirname(__file__))
                fig.savefig(absolute_path+'/lidar.png')
                avoid = basic_detector.main()
                
                if avoid == "avoid":
                    print("")
                else :
                    print("")
                    i=i+1
                    
                    
        # stop thread
        scanner.stop = True


if __name__ == "__main__":
    # create instance of Test class
    #SerialClass = serial_test.SerialControl()
    #SerialClass = SerialControl()
    #asyncio.run(SerialClass.SendCommand("led:1.00:1.00:1.00"))
    
    scanner = LidarScan()
    scanner.main_thread()
    # start thread
