import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import time
import asyncio
import os

def main():
    absolute_path = os.path.abspath(os.path.dirname(__file__))
    
    while not os.path.exists(absolute_path+'/lidar.png'):
        time.sleep(0.05)
    lidar_img = cv2.imread(absolute_path+'/lidar.png')
    
    #get the position of the red dot
    red_dot = np.where(np.all(lidar_img == (0, 0, 255), axis=-1))
    #print(red_dot)
    xlidar = red_dot[1][0]
    ylidar = red_dot[0][0]
    #cv2.circle(lidar_img, (xlidar, ylidar), 10, (0, 255, 0), 0)
    
    #dilate and erode the image to get rid of noise
    kernel = np.ones((1,1),np.uint8)
    lidar_img = cv2.dilate(lidar_img,kernel,iterations = 1)
    lidar_img = cv2.erode(lidar_img,kernel,iterations = 1)
    
    #get the coordinates of all countours
    gray = cv2.cvtColor(lidar_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, (50), 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #draw all contours
    #cv2.drawContours(lidar_img, contours, -1, (0, 255, 0), 3)
    
    #get the distance from the lidar to all contours
    
    close_object_found = False
    for cnt in contours:
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            dist = np.sqrt((cx - xlidar)**2 + (cy - ylidar)**2)
            angle = np.arctan2(cy - ylidar, cx - xlidar)
            if 10<dist < 60 :
                #and 0.6<angle<1.2
                close_object_found = True 
                #print(dist)
                cv2.line(lidar_img, (xlidar, ylidar), (cx, cy), (0, 255, 0), 1)
                #.putText(lidar_img, str(dist), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    if close_object_found:
        print('Close object found')
    else:
        print('No close object found')
    
    #print(time.time()-begin)

    
    
    #cv2.imshow('Lidar', lidar_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()   

if __name__ == '__main__':
    main()
