import pygame
import os
import time


class Sound:

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.s = []
        self.s.append(pygame.mixer.Sound(dir_path + "\\Sound\\1.wav"))
        self.s.append(pygame.mixer.Sound(dir_path + "\\Sound\\2.wav"))
        self.s.append(pygame.mixer.Sound(dir_path + "\\Sound\\3.wav"))

    def play(self, id, wait=True):
        self.s[id].play()
        if wait:
            time.sleep(1)
