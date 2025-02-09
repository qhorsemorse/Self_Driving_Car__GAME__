import pyautogui as py
import time
class CarCommands:
    def __init__(self):
        pass

    @staticmethod
    def accellerate(hold_time=1):
        # click()
        start = time.time()
        while time.time() - start < hold_time:
            py.keyDown('w')
        py.keyUp('w')

    @staticmethod
    def breaks(hold_time=1):
        # click()
        start = time.time()
        while time.time() - start < hold_time:
            py.keyDown(' ')
        py.keyUp(' ')

    @staticmethod
    def turnLeft(hold_time=1):
        # click()
        start = time.time()
        while time.time() - start < hold_time:
            py.keyDown('a')
        py.keyUp('a')

    @staticmethod
    def turnRight(hold_time=1):
        # click()
        start = time.time()
        while time.time() - start < hold_time:
            py.keyDown('d')
        py.keyUp('d')