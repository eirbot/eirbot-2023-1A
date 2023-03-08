import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
import time

# fonction asynchrone pour suivre une ligne noire sur fond blanc
def followLine():
    # initialisation de la caméra
    
    #cap= cv2.VideoCapture(0)
    cap = cv2.imread('C:/Users/arthu/Documents/GitHub/eirbot-2023-1A/robot/test2.jpg')
    cap = cv2.resize(cap, (640, 480))
    gray = cv2.cvtColor(cap,cv2.COLOR_BGR2GRAY)

    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(cap) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

    #for line in lines:
    #    for x1,y1,x2,y2 in line:
    #        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

    sx1=0
    sx2=0
    sy1=0
    sy2=0
    #spritntf pour vider buffer
    for line in lines:
        for x1,y1,x2,y2 in line:
            sx1=sx1+x1
            sx2=sx2+x2
            sy1=sy1+y1
            sy2=sy2+y2
    sx1=sx1/len(lines)
    sx2=sx2/len(lines)
    sy1=sy1/len(lines)
    sy2=sy2/len(lines)
    cv2.line(line_image,(int(sx1),int(sy1)),(int(sx2),int(sy2)),(255,0,0),5)
    #cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)

    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(cap, 0.8, line_image, 1, 0)
    cv2.imshow('image',lines_edges)
    cv2.waitKey(0)
followLine()