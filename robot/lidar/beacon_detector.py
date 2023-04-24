import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import time
import asyncio

def main():
    
    t1 = time.time()
    #load image
    img = cv2.imread('./lidar.png')
    img = cv2.resize(img, (640, 480))
    
    cv2.imshow('image',img)
    cv2.waitKey(0)
    
    #find robot position
    lower_red = np.array([0, 0, 200], dtype = "uint8") 
    upper_red= np.array([0, 0, 255], dtype = "uint8")
    mask = cv2.inRange(img, lower_red, upper_red)
    robotPosition = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0][0][0]
    x = robotPosition[0]
    y = robotPosition[1]
    img = cv2.circle(img, (x, y), radius=0, color=(0, 0, 255), thickness=6)
    
    kernel = np.ones((3, 3), np.uint8)
    #img = cv2.dilate(img, kernel, iterations=1)  
    img= cv2.erode(img, kernel, iterations=1)
    #cv2.imshow('img', img)
    #cv2.waitKey(0)

    # read input and template image (only take template with 1 rotation)
    templatelist = [ ('C:/Users/arthu/Documents/GitHub/eirbot-2023-1A/robot/lidar/template.png', 15, 15, 0.9),('C:/Users/arthu/Documents/GitHub/eirbot-2023-1A/robot/lidar/template_face_hor.png', 15, 15, 0.9),('C:/Users/arthu/Documents/GitHub/eirbot-2023-1A/robot/lidar/template4.png', 15, 15, 0.8),('C:/Users/arthu/Documents/GitHub/eirbot-2023-1A/robot/lidar/template5.png', 20, 20, 0.8)]
    pts=[]
    for template in templatelist:
        
        xresized = template[1]
        yresized = template[2]
        threshold = template[3]
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template[0],0)
        template=cv2.resize(template, (xresized, yresized))
        w, h = template.shape[::-1]
        # Apply template Matching
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
    
        for p in zip(*loc[::-1]):
            #cv2.rectangle(img, p, (p[0] + w, p[1] + h), (255,0,0), 1) 
            #print(type(p))
            cX=int(p[0]+w/2)
            cY=int(p[1] + h/2)
            pts.append([cX,cY])
            #print([cX, cY])
    
    #pts = np.array(pts, np.int32)
    #print(pts)
    tr=[]
    for p in pts:
        for p1 in pts:
            for p2 in pts:
                tr=[p,p1,p2]
                if 6800>cv2.contourArea(np.array(tr, np.int32)) > 6000:
                    print(cv2.contourArea(np.array(tr, np.int32)))
                    cv2.polylines(img, [np.array(tr, np.int32)], isClosed=True, color=(255, 0, 0), thickness=1)
        #cv2.line(img, (x, y), (p[0], p[1]), (0, 255, 0), 1)
    #cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)
    
        
    '''
    #detect contours
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    edges= cv2.Canny(gray, 50,200)  
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    areas = [cv2.contourArea(c) for c in contours]
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)

    
    balise = []
    
    seuilMin =10
    seuilMax = 30
    for c in list(sorted_contours):
        
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)

        #and (len(approx) in [6,7,8,9,10,11,12])
        if cv2.contourArea(c) > seuilMin and cv2.contourArea(c) < seuilMax :
            balise.append(c)
            
    for c in balise:#draw the contour of each potential balise
        cv2.drawContours(img, c, -1, (255,0,0),2)  

            #calculate the center of the contour
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), radius=0, color=(0, 255, 0), thickness=6)
    
        cv2.line(img, (x, y), (cX, cY), (255, 0, 0), 1)

    smallest_item = balise[0]
    

    
    #draw distance to the balise
    '''   
    
    t2 = time.time()
    cv2.imshow('image',img)
    cv2.waitKey(0)
    print(t2-t1)

if __name__ == '__main__':
    main()
