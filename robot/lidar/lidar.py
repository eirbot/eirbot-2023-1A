'''Animates distances and measurment quality'''
from rplidar import RPLidar
from rplidar import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import asyncio
import serial.tools.list_ports


DMAX = 1000
IMIN = 0
IMAX = 200
"""
fig = plt.figure()
ax = plt.subplot(111, projection='polar')
line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
ax.set_rmax(DMAX)
ax.grid(True)
ax.axis('off')
#add a red dot at the center of the lidar with polar coordinates (0,0)
ax.add_patch(plt.Circle((0, 0), 10, color='r', fill=True))"""

def init_lidar():
    print("Listing ports---")
    ports = serial.tools.list_ports.comports()
    for port in ports:
            if "Silicon Labs" in port.description:
                    print("Found Lidar port:", port.device)
                    PORT_NAME = port.device
    lidar = RPLidar(PORT_NAME)
    lidar.connect()
    lidar.clean_input()
    lidar.motor_speed = MAX_MOTOR_PWM
    iterator = lidar.iter_scans()
    return lidar, iterator

def dumb_scan(iterator):
    next(iterator)
    return iterator

def update_line(num, iterator):
    #patches = []
    #patches.append(ax.add_patch(plt.Circle((0, 0), 1000, color='r', fill=False)))
    scan = next(iterator)
    offsets = np.array([(np.radians(-meas[1]), meas[2]) for meas in scan])
    
    
    intens = np.array([meas[0] for meas in scan])

    
    ##################
    #min_idx = np.argmin(np.linalg.norm(intens))
    ##################
    
    #fig.savefig('robot/lidar/lidar.png')
    
    return intens, offsets

def stop_lidar(lidar):
    lidar.stop()
    lidar.disconnect()

def get_scan_var(iterator):
    #lidar, iterator = init_lidar()
    intens, offsets = update_line(0, iterator)
    #line.set_offsets(offsets)
    #line.set_array(intens)
    #fig.savefig('robot/lidar/lidar.png')
    #print('done')

    #stop_lidar(lidar)
    return intens, offsets

if __name__ == '__main__':
    lidar, iterator = init_lidar()
    get_scan_var(iterator)

    #ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=50)
    #plt.show()