#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
# 
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
#   1. git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
#   2. cd xArm-Python-SDK
#   3. python setup.py install
"""
import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
from xarm import version
from xarm.wrapper import XArmAPI


class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 20
        self._angle_acc = 500
        self._vars = {}
        self._funcs = {
            "Custom zero point": self.function_5,
            "Pin7": self.function_12,
            "Pin15": self.function_20,
            "Pin16": self.function_21,
            "Pin1": self.function_6,
            "Back zero": self.function_1,
            "Pin3": self.function_8,
            "Check potting": self.function_3,
            "Pin8": self.function_13,
            "Pin10": self.function_15,
            "Pin2": self.function_7,
            "Pin6": self.function_11,
            "Pin12": self.function_17,
            "Pin14": self.function_19,
            "Pin4": self.function_9,
            "Pin11": self.function_16,
            "Going back movement": self.function_2,
            "Pin9": self.function_14,
            "Pin5": self.function_10,
            "Alert for potting": self.function_4,
            "Pin13": self.function_18,
        }
        self._robot_init()

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def arm(self):
        return self._arm

    @property
    def VARS(self):
        return self._vars

    @property
    def FUNCS(self):
        return self._funcs

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False

    def function_1(self):
        """
        Describe this function...
        """
        while self.is_alive and not (self._arm.get_cgpio_digital(2)[1]):
            t1 = time.monotonic()
            if self._arm.get_cgpio_digital(2)[1]:
                code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'):
                    return
                break
            code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.5)
            code = self._arm.set_cgpio_digital(8, 0, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.1)
            code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.5)
            code = self._arm.set_cgpio_digital(8, 0, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.1)
            interval = time.monotonic() - t1
            if interval < 0.01:
                time.sleep(0.01 - interval)
        self.function_2()
        if not self.is_alive:
            return

    def function_2(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[336.3, 368.8, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[237.4, 523.8, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[87.5, 628.0, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-83.4, 687.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-263.2, 655.3, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-416.4, 556.5, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-521.9, 408.6, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-560.0, 231.0, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-530.0, 55.5, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-434.7, -97.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-284.2, -201.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[-97.8, -265.1, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[82.1, -232.6, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[232.5, -133.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[336.4, 17.1, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        code = self._arm.set_position(*[364.2, 195.3, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return

    def function_3(self):
        """
        Describe this function...
        """
        if self._arm.get_cgpio_digital(1)[1]:
            pass
        else:
            self.function_4()
            if not self.is_alive:
                return

    def function_4(self):
        """
        Describe this function...
        """
        while self.is_alive and not (self._arm.get_cgpio_digital(1)[1]):
            t1 = time.monotonic()
            if self._arm.get_cgpio_digital(1)[1]:
                code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'):
                    return
                break
            code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.5)
            code = self._arm.set_cgpio_digital(8, 0, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            time.sleep(0.5)
            interval = time.monotonic() - t1
            if interval < 0.01:
                time.sleep(0.01 - interval)

    def function_5(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[136.0, 215.3, 620.8, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return

    def function_6(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[364.2, 195.3, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([367.7, 245.3, 442.3, 180.0, 0.0, 0.0], [360.7, 245.3, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_11(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-284.2, -201.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-280.7, -151.9, 442.3, 180.0, 0.0, 0.0], [-287.7, -151.9, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_16(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-416.4, 556.5, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-412.9, 606.5, 442.3, 180.0, 0.0, 0.0], [-419.9, 606.5, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_21(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[336.3, 368.8, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([339.8, 418.8, 442.3, 180.0, 0.0, 0.0], [332.8, 418.8, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_7(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[336.4, 17.1, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([339.9, 57.1, 442.3, 180.0, 0.0, 0.0], [332.9, 57.1, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_12(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-434.7, -97.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-431.2, -47.9, 442.3, 180.0, 0.0, 0.0], [-438.2, -47.9, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_17(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-263.2, 655.3, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-259.7, 705.3, 442.3, 180.0, 0.0, 0.0], [-266.7, 705.3, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_8(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[232.5, -133.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([236.0, -83.9, 442.3, 180.0, 0.0, 0.0], [229.0, -83.9, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_13(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-530.0, 55.5, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-526.5, 105.5, 442.3, 180.0, 0.0, 0.0], [-533.5, 105.5, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_18(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-83.4, 687.9, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-79.9, 737.9, 442.3, 180.0, 0.0, 0.0], [-86.9, 737.9, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_9(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[82.1, -232.6, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([85.6, -182.6, 442.3, 180.0, 0.0, 0.0], [78.6, -182.6, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_14(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-560.0, 231.0, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-556.5, 281.0, 442.3, 180.0, 0.0, 0.0], [-563.5, 281.0, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_19(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[87.5, 628.0, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([91.0, 678.0, 442.3, 180.0, 0.0, 0.0], [84.0, 678.0, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_10(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-97.8, -265.1, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-94.3, -215.1, 442.3, 180.0, 0.0, 0.0], [-101.3, -215.1, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_15(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[-521.9, 408.6, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([-518.4, 458.6, 442.3, 180.0, 0.0, 0.0], [-525.4, 458.6, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    def function_20(self):
        """
        Describe this function...
        """
        code = self._arm.set_position(*[237.4, 523.8, 442.3, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
        if not self._check_code(code, 'set_position'):
            return
        time.sleep(1)
        code = self._arm.move_circle([240.9, 573.8, 442.3, 180.0, 0.0, 0.0], [233.9, 573.8, 442.3, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)
        if not self._check_code(code, 'move_circle'):
            return

    # Robot Main Run
    def run(self):
        try:
            self._tcp_speed = 1000
            self._tcp_acc = 400
            code = self._arm.set_cgpio_digital(8, 0, delay_sec=0)
            if not self._check_code(code, 'set_suction_cup'):
                return
            self.function_5()
            if not self.is_alive:
                return
            while self.is_alive:
                t1 = time.monotonic()
                while self.is_alive and self._arm.get_cgpio_digital(0)[1]:
                    t1 = time.monotonic()
                    code = self._arm.set_cgpio_digital(8, 1, delay_sec=0)
                    if not self._check_code(code, 'set_suction_cup'):
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_6()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_7()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_8()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_9()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_10()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_11()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_12()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_13()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_14()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_15()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_16()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_17()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_18()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_19()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_20()
                    if not self.is_alive:
                        return
                    self.function_3()
                    if not self.is_alive:
                        return
                    self.function_21()
                    if not self.is_alive:
                        return
                    self.function_1()
                    if not self.is_alive:
                        return
                    break
                    interval = time.monotonic() - t1
                    if interval < 0.01:
                        time.sleep(0.01 - interval)
                code = self._arm.set_cgpio_digital(8, 0, delay_sec=0)
                if not self._check_code(code, 'set_suction_cup'):
                    return
                interval = time.monotonic() - t1
                if interval < 0.01:
                    time.sleep(0.01 - interval)
        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)


if __name__ == '__main__':
    RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.213', baud_checkset=False)
    robot_main = RobotMain(arm)
    robot_main.run()
+