import cozmo
import time
import threading
from CuteCozmoSing import CozmoSingleton


class Notes(CozmoSingleton):

    def __init__(self, robot: cozmo.robot.Robot, simple_mode=False):
        CozmoSingleton.__init__(self, robot)
        threading.Thread.__init__(self)
        self.simple_mode = simple_mode

    def play_complete_note(self, note: int):
        # On verifie que le parametre est correct
        if note < 0 or note > 7:
            time.sleep(1)
            return
        # Recuperation du cube et de la couleur correspondant a la note
        cube_number = self.get_cube_number(note)
        print(cube_number)
        cube = self.cubes[cube_number]
        color = self.lights[note]
        # colorie le cube, joue le son, et fait un tap au Cozmo
        cube.set_lights(color)
        self.sound.play(note)
        time.sleep(0.5)
        cube.set_lights(cozmo.lights.off_light)

    def get_cube_number(self, note: int):
        if self.simple_mode:
            return note % 3
        mod = note % 7
        if mod == 0 or mod == 1:
            return 0
        if mod == 2 or mod == 3 or mod == 4:
            return 1
        if mod == 5 or mod == 6:
            return 2
"""
    def lightning_cube(self, cube, color):
        cube.set_lights(color)

    def play_sound(self, note: int):
        if note < 1 or note > 88:
            return
        self.sound.play(note)
"""