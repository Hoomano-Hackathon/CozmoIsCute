import pygame
import os
import time


class Sound:

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.s = []
        for filename in os.listdir(os.path.join(dir_path, "Sound")):
            self.s.append(pygame.mixer.Sound(os.path.join(dir_path, "Sound", filename)))

    def play(self, id, wait=True):
        self.s[id].play()
        if wait:
            time.sleep(1)
