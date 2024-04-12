import os
import time

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
    
    def check_potting(self): #### ASK ABOUT THIS ####       
        while self.arm.get_cgpio_digital(1)[1]:
            self.arm.set_cgpio_digital(8, 1, delay_sec=0)
            time.sleep(0.5)
            self.arm.set_cgpio_digital(8, 0, delay_sec=0)
            time.sleep(0.5)
        else:
            self.arm.set_cgpio_digital(8, 1, delay_sec=0)
    
    def calculate_poses_for_circle(self, diameter, starting_position): # This function is used to calculate the poses for the circle
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

    def move_circle_with_diameter(self, diameter, starting_position): # This function is used to move the robot in a circle
        # Calculate poses based on diameter
        pose1, pose2 = self.calculate_poses_for_circle(diameter, starting_position)

        print("Moving circle with diameter: ", diameter)
        self.arm.move_circle(pose1=pose1, pose2=pose2, percent=100, speed=100, mvacc=100, wait=True)
        print("Circle moved")

# Start of the functions for the pins

    def pin1(self):
        self.arm.set_position(x=364.2, y=195.3, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [367.7, 245.3, 442.3, 180, 0, 0])

    def pin2(self):
        self.arm.set_position(x=336.4, y=17.1, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [339.9, 57.1, 442.3, 180, 0, 0])        
    
    def pin3(self):
        self.arm.set_position(x=232.5, y=-133.9, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [236.0, -83.9, 442.3, 180, 0, 0])

    def pin4(self):
        self.arm.set_position(x=81.2, y=-232.6, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [85.6, -182.6, 442.3, 180, 0, 0])

    def pin5(self):
        self.arm.set_position(x=-97.8, y=-265.1, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-94.3, -215.1, 442.3, 180, 0, 0])

    def pin6(self):
        self.arm.set_position(x=-284.2, y=-201.9, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-280.7, -151.9, 442.3, 180, 0, 0])

    def pin7(self):
        self.arm.set_position(x=-434.7, y=-97.9, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-431.2, -47.9, 442.3, 180, 0, 0])

    def pin8(self):
        self.arm.set_position(x=-530.0, y=55.5, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-526.5, 105.5, 442.3, 180, 0, 0])

    def pin9(self):
        self.arm.set_position(x=-560.0, y=231.0, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-556.5, 281.0, 442.3, 180, 0, 0])

    def pin10(self):
        self.arm.set_position(x=-521.9, y=408.6, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-518.4, 458.6, 442.3, 180, 0, 0])

    def pin11(self):
        self.arm.set_position(x=-416.4, y=556.5, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-412.9, 606.5, 442.3, 180, 0, 0])

    def pin12(self):
        self.arm.set_position(x=-263.2, y=655.3, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-259.7, 705.3, 442.3, 180, 0, 0])

    def pin13(self):
        self.arm.set_position(x=-83.4, y=687.9, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [-79.9, 737.9, 442.3, 180, 0, 0])

    def pin14(self):
        self.arm.set_position(x=87.5, y=628.0, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [91.0, 678.0, 442.3, 180, 0, 0])

    def pin15(self):
        self.arm.set_position(x=237.4, y=523.8, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [240.9, 573.8, 442.3, 180, 0, 0])

    def pin16(self):
        self.arm.set_position(x=336.3, y=368.8, z=442.3, roll=180, pitch=0, yaw=0, speed=speed, mvacc=tcp_acc, is_radian=False, wait=False)
        time.sleep(1)
        self.move_circle_with_diameter(100, [339.8, 418.8, 442.3, 180, 0, 0])

    def back_to_zero(self):
        while not self.arm.get_cgpio_digital(2)[1]:
            t1 = time.monotonic()

            self.arm.set_cgpio_digital(8, 1, delay_sec=0)
            time.sleep(0.5)

            self.arm.set_cgpio_digital(8, 0, delay_sec=0)
            time.sleep(0.1)

            self.arm.set_cgpio_digital(8, 1, delay_sec=0)
            time.sleep(0.5)

            self.arm.set_cgpio_digital(8, 0, delay_sec=0)
            time.sleep(0.1)

            interval = time.monotonic() - t1
            if interval < 0.01:
                time.sleep(0.01 - interval)

        _, current_angle = self.arm.get_servo_angle()
        new_angle = current_angle.copy()

        for i in range(-100, 100, 1): #### ASK ABOUT THIS ####
            new_angle[0] = i
            self.arm.set_servo_angle(new_angle, speed=speed, mvacc=tcp_acc, wait=True)
    
    def run(self):
        self.arm.set_cgpio_digital(8, 0, delay_sec=0)

        self.custom_zero()

        while self.arm.get_cgpio_digital(0)[1]:
            self.arm.set_cgpio_digital(8, 1, delay_sec=0)

            self.check_potting()
            self.pin1()
            self.check_potting()
            self.pin2()
            self.check_potting()
            self.pin3()
            self.check_potting()
            self.pin4()
            self.check_potting()
            self.pin5()
            self.check_potting()
            self.pin6()
            self.check_potting()
            self.pin7()
            self.check_potting()
            self.pin8()
            self.check_potting()
            self.pin9()
            self.check_potting()
            self.pin10()
            self.check_potting()
            self.pin11()
            self.check_potting()
            self.pin12()
            self.check_potting()
            self.pin13()
            self.check_potting()
            self.pin14()
            self.check_potting()
            self.pin15()
            self.check_potting()
            self.pin16()

            self.back_to_zero()
            break
        
        self.arm.set_cgpio_digital(8, 0, delay_sec=0)
