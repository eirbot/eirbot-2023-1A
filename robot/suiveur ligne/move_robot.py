"""
Correction module for line following
Pompé sur Seb le bg toujours
"""
import math
import time
import asyncio
from suiveur_ligne import Detection, Color


class Robot:
    """
    robot class with motors and detection initialization
    """

    def __init__(self, average_speed):
        self.detection = Detection()

        self.previous_error = 0
        self.average_speed = average_speed  # degrés/secondes
        self.tmp_prev = time.time()

    async def tick(self, color):
        """
        A method for doing the necessary processing for a line-following tick. This method must be encapsulated in a
        while true to allow optimal line tracking
        :param color: The color to follow
        :return: None
        """
        cx, cy,img_width, img_height = await self.detection.detect(color)
        if cx != 0 and cy != 0:
            # error is the distance between the center of the line and the center of the image
            # je pense que c'est le centre de l'image donc shape/2
            #print(img_width)
            #error = cx - img_width / 2

            # Define the three points
            top_middle = (img_width / 2, 0)
            bottom_middle = (img_width / 2, img_height)
            center = (cx, cy)

            # Calculate the vectors
            vector1 = (bottom_middle[0] - top_middle[0], bottom_middle[1] - top_middle[1])
            vector2 = (bottom_middle[0] - center[0], bottom_middle[1] - center[1])

            # Calculate the dot product
            dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]

            # Calculate the magnitudes
            magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
            magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

            # Calculate the angle in radians
            angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))

            # Convert the angle to degrees
            #angle_deg = math.degrees(angle_rad)

            # Print the angle
            print("angle",angle_rad)
            # à adapter
            #await serial_write(error)
            return cx, cy, angle_rad
    
    def calcul_center_camera(self, height, width):
        """
        Calcul the center of the camera from height and width
        :return: center of the camera
        """
        x = width / 2
        y = height / 2
        return x, y
            
    async def tick_tock(self, color, running_time):
        """
        Encapsulates the tick method in a while true sensitive to keyboard interrupts
        :param color: The color to follow
        :param running_time: time before stop while loop
        :return: None
        """
        begin = time.time()
        try:
            while time.time() - begin < running_time:
                x_center_line, y_center_line, corr_angle_rad = await self.tick(color)
        except KeyboardInterrupt:
            print("Stopped")
            return

async def main(color, running_time):
    """
    Main method for line following
    :param color: The color to follow
    :return: None
    """
    robot = Robot(500)
    await robot.tick_tock(color, running_time)


if __name__ == "__main__":
    asyncio.run(main(Color.BLACK, 5))