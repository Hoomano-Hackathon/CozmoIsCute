import cozmo
import time
from sound_player import Sound
import threading


class Notes(threading.Thread):

    def __init__(self, sound: Sound, cubes: [], lights: [cozmo.lights.Light]):
        threading.Thread.__init__(self)
        self.sound = sound
        self.cubes = cubes
        self.lights = lights
        self.nb_notes = len(lights)

    def play_complete_note(self, note: int):
        # On verifie que le parametre est correct
        if note < 0 or note > 88:
            return
        # Recuperation du cube et de la couleur correspondant a la note
        cube_number = self.get_cube_number(note)
        cube = self.cubes[cube_number]
        color = self.lights[note % self.nb_notes]
        # colorie le cube, joue le son, et fait un tap au Cozmo
        cube.set_lights(color)
        self.sound.play(note)
        time.sleep(1)
        cube.set_lights(cozmo.lights.off_light)

    def get_cube_number(self, note: int):
        mod = note % self.nb_notes
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