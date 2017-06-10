import cozmo
import asyncio
from cozmo.util import Angle

import pygame
import threading
from queue import Queue
from CuteCozmoSing import CozmoSingleton
from Notes import Notes

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

    def wait_for_note(self, note, timeout=5):
        pass  # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True


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
