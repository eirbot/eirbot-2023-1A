#!/usr/bin/env python3
'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import serial.tools.list_ports
import os
import threading
import time

print("Listing ports---")
ports = serial.tools.list_ports.comports()
for port in ports:
        if "Silicon Labs" in port.description:
                print("Found Lidar port:", port.device)
                PORT_NAME = port.device
DMAX = 1000
IMIN = 0
IMAX = 200

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    fig.savefig(absolute_path+'/lidar.png')

    return line,

def lidar_animation_thread():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    ax.axis('off')
    ax.add_patch(plt.Circle((0, 0), 10, color='r', fill=True))

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)

    # Save the figure
    def save():
        absolute_path = os.path.abspath(os.path.dirname(__file__))
    lidar.stop()
    lidar.disconnect()


# Start the threads
def main(lidar_animation_thread,response_thread):
    lidar_animation_thread = threading.Thread(target=lidar_animation_thread)
    response_thread = threading.Thread(target=response_thread)
    lidar_animation_thread.start()
    response_thread.start()
    
main(lidar_animation_thread, response_thread)
