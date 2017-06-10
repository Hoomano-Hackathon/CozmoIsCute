import pygame
import os
import time


NB_MUSICS = 64

class Sound:

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.s = []
        files = os.listdir(os.path.join(dir_path, "Sound"))
        files.sort()
        for filename in files:
            self.s.append(pygame.mixer.Sound(os.path.join(dir_path, "Sound", filename)))
        # print(self.s)

    def play(self, id, wait=False):
        self.s[id].play()
        if wait:
            time.sleep(1)
