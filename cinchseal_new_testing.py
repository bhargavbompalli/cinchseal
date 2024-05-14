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
from xarm.wrapper import XArmAPI


class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self._last_completed_step = 0
        self.is_paused = False
        self.alive = True
        self._arm = robot
        self._tcp_speed = 60
        self._tcp_acc = 2000
        self._angle_speed = 20
        self._angle_acc = 500
        self._variables = {}
        self._robot_init()
        self._cgpio_digital_callbacks = []
        self._cgpio_state = None
        self._callback_in_thread = kwargs.get('callback_in_thread', True)
        self._callback_que = queue.Queue()
        gpio_t = threading.Thread(target=self._listen_gpio_thread, daemon=True)
        gpio_t.start()
        callback_t = threading.Thread(target=self._event_callback_handle_thread, daemon=True)
        callback_t.start()

    def _event_callback_handle_thread(self):
        while self.alive:
            try:
                callback = self._callback_que.get(timeout=1)
                callback() if not self._callback_in_thread else threading.Thread(target=callback, daemon=True).start()
            except queue.Empty:
                pass
            except Exception as e:
                self.pprint(e)

    def _listen_gpio_thread(self):
        _, values = self._arm.get_cgpio_state()
        cgpio_digitals = [values[3] >> i & 0x0001 if values[10][i] in [0, 255] else 1 for i in range(len(values[10]))] if _ == 0 else [0] * 16
        while self.alive:
            _, values = self._arm.get_cgpio_state()
            if _ == 0 and self._cgpio_state is not None and self._cgpio_state != values:
                digitals = [values[3] >> i & 0x0001 if values[10][i] in [0, 255] else 1 for i in range(len(values[10]))]
                for item in self._cgpio_digital_callbacks:
                    for io in range(len(digitals)):
                        if item['io'] == io and eval('{} {} {}'.format(digitals[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(cgpio_digitals[io], item['op'], item['trigger'])):
                            self._callback_que.put(item['callback'])
                cgpio_digitals = digitals
            self._cgpio_state = values if _ == 0 else self._cgpio_state
            time.sleep(0.01)

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

    # Define Contoller GPIO-1 DIGITAL is HIGH callback
    def controller_gpio_1_digital_is_changed_callback_1(self):
        self.is_paused = False
        self.execute_movements()

    # Define Contoller GPIO-1 DIGITAL is LOW callback
    def controller_gpio_1_digital_is_changed_callback_2(self):
        self.is_paused = True

    def execute_movements(self):
        steps = [self.step1, self.step2, self.step3]

        for step in steps[self._last_completed_step:]:
            if not self.is_paused:
                break
            step()
            self._last_completed_step += 1
            if self._last_completed_step >= len(steps):
                self._last_completed_step = 0
    
    def step1(self):
        self._arm.set_position(*[412.8, -184.2, 450.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)
    
    def step2(self):
        self._arm.set_position(*[412.8, -184.2, 350.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)

    def step3(self):
        self._arm.move_circle([260.4, -106.2, 550.0, 180.0, 0.0, 0.0], [376.2, -19.2, 350.0, 180.0, 0.0, 0.0], float(360) / 360 * 100, speed=self._tcp_speed, mvacc=self._tcp_acc, wait=True)

    def step4(self):
        self._arm.set_position(*[412.8, -184.2, 450.0, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=-1.0, wait=True)

    # Robot Main Run
    def run(self):
        self._cgpio_digital_callbacks.append({'io': 1, 'trigger': 1, 'op': '==', 'callback': self.controller_gpio_1_digital_is_changed_callback_1})
        self._cgpio_digital_callbacks.append({'io': 1, 'trigger': 0, 'op': '==', 'callback': self.controller_gpio_1_digital_is_changed_callback_2})
        while True:
            if not self.is_paused:
                self.execute_movements()
            time.sleep(1)

if __name__ == '__main__':
    arm = XArmAPI('192.168.1.240', baud_checkset=False)
    robot_main = RobotMain(arm)
    robot_main.run()
