'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM8'
DMAX = 4000
IMIN = 0
IMAX = 50


lidar = RPLidar(PORT_NAME)
fig = plt.figure()
ax = plt.subplot(111, projection='polar')
line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
ax.set_rmax(DMAX)
ax.grid(True)
ax.axis('off')
#add a red dot at the center of the lidar with polar coordinates (0,0)
ax.add_patch(plt.Circle((0, 0), 10, color='r', fill=True))


def update_line(num, iterator, line):
    
    #patches = []
    #patches.append(ax.add_patch(plt.Circle((0, 0), 1000, color='r', fill=False)))
    
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    
    intens = np.array([meas[0] for meas in scan])
    
    line.set_array(intens)
    
    ##################
    #min_idx = np.argmin(np.linalg.norm(intens))
    ##################
    
    fig.savefig(f'lidar.png')
    
    return line,#patches

iterator = lidar.iter_scans()
ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=50)

plt.show()

lidar.stop()
lidar.disconnect()


