import os

from xarm.wrapper import XArmAPI

ip = "192.168.1.213" # Please change to the IP of your robot

speed = 100 # Please change speed of the robot, in mm/s
tcp_acc = 2000 # Please change the TCP acceleration of the robot, in mm/s^2

class CinchSeal:
    def __init__(self, ip):
        self.arm = XArmAPI(ip)
        self.arm.motion_enable(enable=True)
        self.arm.set_mode(0)
        self.arm.set_state(0)
        self.speed = 100 # Example speed, in mm/s
        self.tcp_acc = 2000 # Example acceleration, in mm/s^2

    def custom_zero(self):
        self.arm.set_position(x=136.0, y=215.3, z=620.8, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
    
    def check_potting(self):
        #THIS SHOULD INCLUDE ALERT FOR POTTING LOGIC
    
    def calculate_poses_for_circle(diameter, starting_position):
        radius = diameter / 2
        print("radius: ", radius)

        center_x, center_y = starting_position[0], starting_position[1] - radius  # Example starting center based on provided poses
        print("center_x: ", center_x)
        print("center_y: ", center_y)

        pose1 = [center_x + radius, center_y, starting_position[2], starting_position[3], starting_position[4], starting_position[5]]  # Z, roll, pitch, and yaw are constant based on the example
        print("pose1: ", pose1)

        pose2 = [center_x - radius, center_y, starting_position[2], starting_position[3], starting_position[4], starting_position[5]]  # Z, roll, pitch, and yaw are constant based on the example
        print("pose2: ", pose2)

        return pose1, pose2

    def move_circle_with_diameter(diameter, starting_position):
        # Calculate poses based on diameter
        pose1, pose2 = calculate_poses_for_circle(diameter, starting_position)

        print("Moving circle with diameter: ", diameter)
        arm.move_circle(pose1=pose1, pose2=pose2, percent=100, speed=100, mvacc=100, wait=True)
        print("Circle moved")

    def pin1(self):
    
    def pin2(self):
    
    def pin3(self):
    
    def pin4(self):
    
    def pin5(self):
    
    def pin6(self):
    
    def pin7(self):

    def pin8(self):

    def pin9(self):

    def pin10(self):

    def pin11(self):

    def pin12(self):

    def pin13(self):

    def pin14(self):

    def pin15(self):

    def pin16(self):

    def back_to_zero(self):
        #THIS SHOULD INCLUDE GOING BACK MOVEMENT