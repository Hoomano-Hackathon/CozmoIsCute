import pygame, sys, os, time
from pygame.locals import *
from sound_player import Sound
import cute_cozmo

# set up pygame
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

dir_path = os.path.dirname(os.path.realpath(__file__))

# set up the colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

print(dir_path)
class KeyboardApp ():
    def __init__(self, cozmo_thread):
        self.cozmo = cozmo_thread
        super(KeyboardApp, self).__init__()
        self.running = False
        self.rect_dict = {}

        # set up the window
        self.windowSurface = pygame.display.set_mode((500, 400), 0, 32)
        pygame.display.set_caption('Cozmo is cute')

        # set up fontsz
        basicFont = pygame.font.SysFont(None, 48)

        # draw the white background onto the surface
        self.windowSurface.fill(WHITE)

        letters = "zqsdfgUD"

        # draw the "keys" on the canvas
        for num in range(0,8):
            rect = pygame.draw.rect(self.windowSurface, BLUE, (20+60*num, 20, 40, 40))
            self.rect_dict[letters[num]] = [rect, num]

        """rect = pygame.draw.rect(windowSurface, BLUE, (80, 20, 40, 40))
        rect_dict["q"] = [rect, 1]

        rect = pygame.draw.rect(windowSurface, BLUE, (140, 20, 40, 40))
        rect_dict["s"] = [rect, 2]"""


        # pygame.draw.rect(windowSurface, BLUE, (rect + 20, rect + 20, 40, 40))
        # get a pixel array of the surface
        pixArray = pygame.PixelArray(self.windowSurface)
        pixArray[480][380] = RED
        del pixArray

        # draw the window onto the screen
        pygame.display.update()

    def stop(self):
        self.running = False
        sys.exit(0)

    def run(self):
        self.running = True
        soundPlayer = Sound()

        # run the game loop
        while self.running:
            # Reset all rect colors
            for key in self.rect_dict:
                self.windowSurface.fill(BLUE, self.rect_dict[key][0])

            # Check current key presses
            for event in pygame.event.get():
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w]:
                    rectProp = self.rect_dict["z"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_a]:
                    rectProp = self.rect_dict["q"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_s]:
                    rectProp = self.rect_dict["s"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_d]:
                    rectProp = self.rect_dict["d"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_f]:
                    rectProp = self.rect_dict["f"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_g]:
                    rectProp = self.rect_dict["g"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_UP]:
                    rectProp = self.rect_dict["U"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_DOWN]:
                    rectProp = self.rect_dict["D"]
                    self.windowSurface.fill(RED, rectProp[0])
                    soundPlayer.play(rectProp[1], False)
                elif pressed[pygame.K_p]:
                    self.stop()

                pygame.display.update()

if __name__ == '__main__':
    cozmo_thread = cute_cozmo.Cozmo_thread()
    cozmo_thread.daemon = True
    cozmo_thread.start()

    ka = KeyboardApp(None)
    ka.run()
