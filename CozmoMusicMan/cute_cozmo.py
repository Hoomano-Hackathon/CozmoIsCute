import cozmo
import time
import asyncio
import math

from enum import Enum
import pygame
import threading
from queue import Queue
from CuteCozmoSing import CozmoSingleton
from Notes import Notes

class CuteCozmo(CozmoSingleton):

'''
Goes in the trigonometric way
'''
class Dir(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

class CuteCozmo(CozmoSingleton):
    def __init__(self, robot: cozmo.robot.Robot):
        CozmoSingleton.__init__(self, robot)
        self.notes = Notes(robot, simple_mode=False)

    def play_partition(self, partition: [int]):
        for note in partition:
            self.play_note(note)

    def play_note(self, note: int):
        if self.notes is not None:
            action = self.hit()
            self.notes.play_complete_note(note)
            action.wait_for_completed()
        else:
            print('no notes in instance !')

    # light a certain cube with the correct color
    def light_led(self, led_index):
        nb_notes = len(self.notes)
        light = self.lights[led_index]
        if len(self.notes) == 3:
            self.cubes[led_index].set_lights(light)
        else:
            cube_index = self.cube_from_note(led_index)
            print('cube_index =', cube_index)
            self.cubes[cube_index].set_lights(light)
        self.robot.set_all_backpack_lights(light)

    def wait_for_note(self, note, timeout=5):
        global q
        # empty the queue
        print('before :', q)
        try:
            while q.get_nowait() is not None:
                pass
        except:
            pass
        print('after :', q)

        # pass # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True
        print('waiting for note', note)
        # code to receive note from MainThread
        print('pre get')
        try:
            playedNote = q.get(timeout=timeout)
        except:
            return False
        print('post get')
        return playedNote == note
        # if playedNote == note:
        #     return True
        # return False


def cozmo_program(robot: cozmo.robot.Robot):
    cute = CuteCozmo(robot)
    cute.hit().wait_for_completed()
    cute.play_partition([0, 1, 2, 3, 4, 5, 6, 7])
    # cute.play_partition([0, 0, 0, 1, 2, -1, 1, 0, 2, 1, 1, 0])


def setup_pygame():
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.update()


class Cozmo_thread(threading.Thread):

    def __init__(self, q1: Queue):
        super().__init__()
        global q
        q = q1

    def run(self):
        cozmo.run_program(cozmo_program)
