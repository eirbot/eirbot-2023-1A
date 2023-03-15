import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import time


def main():
    t1 = time.time()
    #load image
    img = cv2.imread('c:/Users/arthu/Desktop/files/code perso/eirbot/lidar.png')
    img = cv2.resize(img, (640, 480))
    
    #find robot position
    lower_red = np.array([0, 0, 200], dtype = "uint8") 
    upper_red= np.array([0, 0, 255], dtype = "uint8")
    mask = cv2.inRange(img, lower_red, upper_red)
    robotPosition = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0][0][0]
    x = robotPosition[0]
    y = robotPosition[1]
    img = cv2.circle(img, (x, y), radius=0, color=(0, 0, 255), thickness=6)
    
    #detect contours
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    edges= cv2.Canny(gray, 50,200)  
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    areas = [cv2.contourArea(c) for c in contours]
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    
    balise = []
    
    for c in list(sorted_contours):
        if cv2.contourArea(c) > 14 and cv2.contourArea(c) < 20:
            balise.append(c)
            
    for c in balise:
        cv2.drawContours(img, c, -1, (255,0,0),1)  

        
    smallest_item = balise[2]
    
    #calculate the center of the contour
    M = cv2.moments(smallest_item)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(img, (cX, cY), radius=0, color=(0, 255, 0), thickness=6)
    
    #draw distance to the balise
    cv2.line(img, (x, y), (cX, cY), (255, 0, 0), 1)
        
    t2 = time.time()
    cv2.imshow('image',img)
    cv2.waitKey(0)
    print(t2-t1)
    

if __name__ == '__main__':
    main()
