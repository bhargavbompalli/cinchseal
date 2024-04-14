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

speed = 200

def initialize():
    arm.set_cgpio_digital(8, 0, delay_sec=0)
    arm.set_position(*[136, 215.3, 620.8, 180, 0, 0], speed=speed, is_radian=False, wait=True)
    pass

def reset_position():
    arm.set_servo_angle(angle=[3.5, -62.4, -41.9, 0, 104.2, 3.5], speed=50, mvacc=100, wait=True)

def wait_for_start():
    start = 0
    while start == 0:
        code, start = arm.get_cgpio_digital(ionum=0)
        time.sleep(0.1)  # Check every 100ms

def move_arm_sequence():
    # Define a list of positions for the arm to move through
    positions = [
        (400, 254, 400, 180, 0, 0),
        (195, 254, 400, 180, 0, 0),
        (450, 254, 400, 180, 0, 0),
        (400, 254, 400, 180, 0, 0)
    ]
    
    for pos in positions:
    # Check sensor state & reset button state before each move
        while True:
            code, sensor_state = arm.get_cgpio_digital(ionum=1)
            if sensor_state == 0:
                time.sleep(0.1)
                continue

            code, reset = arm.get_cgpio_digital(ionum=2)
            if reset == 1:
                arm.set_cgpio_digital(8, 0, delay_sec=0) #Turn off the LED
                return True
            
            break

        # Move to next position
        arm.set_cgpio_digital(8, 1, delay_sec=0) #Turn on the LED
        arm.set_position(*pos, speed=speed, is_radian=False, wait=True)
    
    last_reset_state = 0
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