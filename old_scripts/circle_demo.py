# This script is used to move the xArm in a circle

from xarm.wrapper import XArmAPI
import numpy as np

ip = "192.168.1.213" #Change this to your xArm IP address

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)

#Here is a function which simplifies the process so you can just input a diameter and the robot will move in a circle
#Type in the starting position and the diameter of the circle you want to move in

starting_position = [378, 254, -9.9, -180, 0, -29.9]  # Example starting position
diameter = 100  # Example diameter, in mm
print("Starting position: ", starting_position)

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

move_circle_with_diameter(diameter, starting_position)