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
        for i in range(1,NB_MUSICS+1):
            self.s.append(pygame.mixer.Sound(os.path.join(dir_path, 'Sound', str(i) + '.wav')))

    def play(self, id, wait=True):
        if id >= 0 and id < NB_MUSICS:
            self.s[id].play()
        if wait:
            time.sleep(1)
