"""
Correction module for line following
Pompé sur Seb le bg toujours
"""
import time

from suiveur_ligne import Detection, Color


class Robot:
    """
    robot class with motors and detection initialization
    """

    def __init__(self, average_speed):
        self.detection = Detection()
        #self.motors = Motors()
        #self.odometry = Odometry()

        # koa??
        self.kp = 0.9
        self.Kd = 0
        self.kpa = 1
        self.kpd = 300
        self.Kp_theta = 100
        #
        self.previous_error = 0
        self.average_speed = average_speed  # degrés/secondes
        self.tmp_prev = time.time()

    def tick(self, color):
        """
        A method for doing the necessary processing for a line-following tick. This method must be encapsulated in a
        while true to allow optimal line tracking
        :param color: The color to follow
        :return: None
        """
        cx, cy,img_width, img_height = self.detection.detect(color)
        if cx != 0 and cy != 0:
            # error is the distance between the center of the line and the center of the image
            # je pense que c'est le centre de l'image donc shape/2
            print(img_width)
            error = cx - img_width / 2
            print(error)
            # à adapter
            '''correction = self.kp * error + self.Kd * (error - self.previous_error) / (time.time() - self.tmp_prev)

            self.previous_error = error
            self.tmp_prev = time.time()

            left_instruction = self.average_speed + correction
            right_instruction = self.average_speed - correction

            if left_instruction > 720:
                right_instruction = right_instruction - (left_instruction - 720)
                left_instruction = 720
            elif left_instruction < -720:
                right_instruction = right_instruction + (-720 - left_instruction)
                left_instruction = -720

            if right_instruction > 720:
                left_instruction = left_instruction - (right_instruction - 720)
                right_instruction = 720
            elif right_instruction < -720:
                left_instruction = left_instruction + (-720 - right_instruction)
                right_instruction = -720
            self.motors.move(left_instruction, right_instruction)
        else:
            self.motors.move(220, 160)
        '''
    def tick_tock(self, color, running_time):
        """
        Encapsulates the tick method in a while true sensitive to keyboard interrupts
        :param color: The color to follow
        :param running_time: time before stop while loop
        :return: None
        """
        begin = time.time()
        try:
            while time.time() - begin < running_time:
                self.tick(color)
        except KeyboardInterrupt:
            print("Stopped")
            return

if __name__ == "__main__":
    robot = Robot(500)
    robot.tick_tock(Color.BLACK, 10)