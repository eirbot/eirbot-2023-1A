"""Premier script pour commencer sur opencv."""
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("image0.jpeg")
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


plt.subplot(1, 1, 1)
plt.imshow(img_rgb)
plt.show()