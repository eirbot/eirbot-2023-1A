"""Premier script pour commencer sur opencv."""
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("image9.jpeg")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

bright_red_lower_bounds = (0, 100, 100)
bright_red_upper_bounds = (10, 255, 255)
bright_red_mask = cv2.inRange(img_hsv, bright_red_lower_bounds, bright_red_upper_bounds)

cv2.imshow("masque clair", bright_red_mask)

dark_red_lower_bounds = (160, 100, 100)
dark_red_upper_bounds = (179, 255, 255)
dark_red_mask = cv2.inRange(img_hsv, dark_red_lower_bounds, dark_red_upper_bounds)

cv2.imshow("masque fonce", dark_red_mask)


weighted_mask = cv2.addWeighted(bright_red_mask, 1.0, dark_red_mask, 1.0, 0.0)
cv2.imshow("addition clair et fonce", weighted_mask)

blurred_mask = cv2.GaussianBlur(weighted_mask,(9,9),3,3)
cv2.imshow("test", blurred_mask)
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
#img_traitee = cv2.erode(img_hsv, kernel, iterations=1)
#cv2.imshow("erodee", img_traitee)


#mask = cv2.inRange(img_hsv, lower_color, upper_color)
#cv2.imshow('mask', mask)
#res = cv2.bitwise_and(img, img_hsv, mask = mask)
#cv2.imshow("b", res)


#img_grise = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#cv2.imshow("gris", img_grise)


plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()