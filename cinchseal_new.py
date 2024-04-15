import os
import sys
import time
import math
import threading

from xarm.wrapper import XArmAPI

ip = "192.168.1.213"

arm = XArmAPI(ip)
arm.motion_enable(enable=True)
arm.set_mode(0)
arm.set_state(state=0)
start = False

speed = 200 # Adjust the speed of the robot, in mm/s
diameter = 100 # Adjust the diameter of the circle, in mm

def initialize(): # Initialize the robot by turning off the LED and moving to the starting position
    arm.set_cgpio_digital(8, 0, delay_sec=0)
    arm.set_position(*[136, 215.3, 620.8, 180, 0, 0], speed=speed, is_radian=False, wait=True)
    pass

def reset_position(): # This is the reset position, bringing the robot back after button is pressed
    arm.set_servo_angle(angle=[3.5, -62.4, -41.9, 0, 104.2, 3.5], speed=50, mvacc=100, wait=True)

def wait_for_start(): # This is a loop which will continue until the start button is pressed
    start = 0
    while start == 0:
        code, start = arm.get_cgpio_digital(ionum=0)
        time.sleep(0.1)  # Check every 100ms

def calculate_poses_for_circle(diameter, starting_position): # This function is used to calculate the poses for the circle
    radius = diameter / 2
    print("radius: ", radius)

    center_x, center_y = starting_position[0], starting_position[1] - radius  
    print("center_x: ", center_x)
    print("center_y: ", center_y)

    pose1 = [center_x + radius, center_y, starting_position[2], starting_position[3], starting_position[4], starting_position[5]] 
    print("pose1: ", pose1)

    pose2 = [center_x - radius, center_y, starting_position[2], starting_position[3], starting_position[4], starting_position[5]] 
    print("pose2: ", pose2)

    return pose1, pose2

def move_circle_with_diameter(diameter, starting_position): # This function is used to move the robot in a circle
    # Calculate poses based on diameter
    pose1, pose2 = calculate_poses_for_circle(diameter, starting_position)

    print("Moving circle with diameter: ", diameter)
    arm.move_circle(pose1=pose1, pose2=pose2, percent=100, speed=50, mvacc=100, wait=True)
    print("Circle moved")

def move_arm_sequence():
    # Define a list of positions and coordinates for the circle for the arm to move through
    positions_and_circles = [
        ((364.2, 195.3, 442.3, 180, 0, 0),(diameter, [367.7, 245.3, 442.3, 180, 0, 0])),
        ((336.4, 17.1, 442.3, 180, 0, 0),(diameter, [339.9, 57.1, 442.3, 180, 0, 0])),
        ((232.5, -133.9, 442.3, 180, 0, 0),(diameter, [236.0, -83.9, 442.3, 180, 0, 0])),
        ((81.2, -232.6, 442.3, 180, 0, 0),(diameter, [85.6, -182.6, 442.3, 180, 0, 0])),
        ((-97.8, -265.1, 442.3, 180, 0, 0),(diameter, [-94.3, -215.1, 442.3, 180, 0, 0])),
        ((-284.2, -201.9, 442.3, 180, 0, 0),(diameter, [-280.7, -151.9, 442.3, 180, 0, 0])),
        ((-434.7, -97.9, 442.3, 180, 0, 0),(diameter, [-431.2, -47.9, 442.3, 180, 0, 0])),
        ((-530.0, 55.5, 442.3, 180, 0, 0),(diameter, [-526.5, 105.5, 442.3, 180, 0, 0])),
        ((-560.0, 231.0, 442.3, 180, 0, 0),(diameter, [-556.5, 281.0, 442.3, 180, 0, 0])),
        ((-521.9, 408.6, 442.3, 180, 0, 0),(diameter, [-518.4, 458.6, 442.3, 180, 0, 0])),
        ((-416.4, 556.5, 442.3, 180, 0, 0),(diameter, [-412.9, 606.5, 442.3, 180, 0, 0])),
        ((-263.2, 655.3, 442.3, 180, 0, 0),(diameter, [-259.7, 705.3, 442.3, 180, 0, 0])),
        ((-83.4, 687.9, 442.3, 180, 0, 0),(diameter, [-79.9, 737.9, 442.3, 180, 0, 0])),
        ((87.5, 628.0, 442.3, 180, 0, 0),(diameter, [91.0, 678.0, 442.3, 180, 0, 0])),
        ((237.4, 523.8, 442.3, 180, 0, 0),(diameter, [240.9, 573.8, 442.3, 180, 0, 0])),
        ((336.3, 368.8, 442.3, 180, 0, 0),(diameter, [339.8, 418.8, 442.3, 180, 0, 0])),
    ]
    
    for pos, circle in positions_and_circles:
    # Check sensor state & reset button state before each move
        while True:
            code, sensor_state = arm.get_cgpio_digital(ionum=1) # Check the sensor state
            if sensor_state == 0:
                time.sleep(0.1)
                continue

            code, reset = arm.get_cgpio_digital(ionum=2) # Check the reset button state
            if reset == 1:
                arm.set_cgpio_digital(8, 0, delay_sec=0) # Turn off the LED
                return True
            
            break

        arm.set_cgpio_digital(8, 1, delay_sec=0) # Turn on the LED

        arm.set_position(*pos, speed=speed, is_radian=False, wait=True) # Move to the position

        move_circle_with_diameter(circle[0], circle[1]) # Move in a circle
    
    last_reset_state = 0 # Once the sequence is complete, wait for the reset button to be pressed
    while True:
        code, reset = arm.get_cgpio_digital(ionum=2)
        if reset == 1 and last_reset_state == 0:
            return True
        last_reset_state = reset
        time.sleep(0.1)

def main():

    initialize()

    while True:
        wait_for_start()
        reset_requested = move_arm_sequence()
        if reset_requested:
            print("Resetting arm")
            reset_position()
            break
        print("Waiting for start button press")

     
if __name__ == "__main__":
    main()