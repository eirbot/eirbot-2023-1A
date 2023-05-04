"""
File for camera treatment and line detection
Adapté de https://github.com/sedelpeuch/Semestre_9
Merci Seb le bg
"""

from enum import Enum

import cv2

# (RED, GREEN, BLUE, BLACK)
Hl = (0,   47,  99, 0)
Sl = (42,  41,  75, 0)
Vl = (87,  0,  65, 0)
Hh = (82,  97,  120, 360)
Sh = (255, 255, 187, 255)
Vh = (255, 255, 255, 50)

# Hl = (0,   47,  99)
# Sl = (61,  41,  75)
# Vl = (0,  0,  65)
# Hh = (255,  97,  120)
# Sh = (212, 255, 187)
# Vh = (235, 255, 255)


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    BLACK = 3

class Detection:
    """
    Class for camera treatment using OpenCV
    """

    def __init__(self):
        self.cap = cv2.VideoCapture('robot/suiveur ligne/line.mp4')

    def detect(self, color):
        """
        Main function for camera treatment, from a video stream it detects the maximum area of the color passed in parameter
        :param color: colour you want to detect
        """
        c_x = 0
        c_y = 0
        print('detecting')
        if (self.cap.isOpened()):
            ret, img = self.cap.read()
            if img is not None:
                
                # rotate image
                img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                
                img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                low_color = (Hl[color.value], Sl[color.value], Vl[color.value])
                high_color = (Hh[color.value], Sh[color.value], Vh[color.value])
                thresh = cv2.inRange(img_hsv, low_color, high_color)

                # get contours and filter on area
                contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = contours[0] if len(contours) == 2 else contours[1]
                # result = img.copy()
                contour = 0
                area_max = 0
                c = None
                for c in contours:
                    area = cv2.contourArea(c)
                    if area > area_max:
                        area_max = area
                        contour = c
                m = None
                if area_max > 0 and c is not None:
                    m = cv2.moments(contour)
                if m is not None and not (m["m00"] == 0):
                    c_x = int(m["m10"] / m["m00"])
                    c_y = int(m["m01"] / m["m00"])

                    '''
                    # see sexy result
                    print(c_x, c_y)
                    # show circle on the center of the detected area
                    cv2.circle(img, (c_x, c_y), 7, (255, 255, 255), -1)

                    # vertical line at the middle of the image using the height and width of the image
                    middle_top_camera = (int(img.shape[1] / 2), 0)
                    middle_bottom_camera = (int(img.shape[1] / 2), img.shape[0])
                    cv2.line(img, middle_top_camera, middle_bottom_camera, (0, 255, 255), 2)
                    cv2.imshow('frame',img)
                    cv2.waitKey(10)
                    '''
                    
            
                width = img.shape[1]
                height = img.shape[0]
            else:
                print("No image")
                width = 0
                height = 0
        return c_x, c_y, width, height

    def __del__(self):
        self.cap.release()


if __name__ == "__main__":
    detection = Detection()
    print(detection.detect(Color.BLACK))