import pygame, sys, os, time
from pygame.locals import *
from sound_player import Sound
import cute_cozmo
from queue import Queue

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

playedNote = 0

print(dir_path)
class KeyboardApp ():
    def __init__(self, cozmo_thread, queue: Queue):
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

        keyCodes = [119, 97, 115, 100, 102, 103, 273, 274, 112]

        # draw the "keys" on the canvas
        for num in range(0,8):
            rect = pygame.draw.rect(self.windowSurface, BLUE, (20+60*num, 20, 40, 40))
            self.rect_dict[keyCodes[num]] = [rect, num]


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
        global playedNote
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
                for key, value in self.rect_dict.items():
                    if pressed[key]:
                        self.windowSurface.fill(RED, value[0])
                        soundPlayer.play(value[1], False)
                        queue.put(key)

                    if pressed[pygame.K_p]:
                        self.stop()

                pygame.display.update()

if __name__ == '__main__':
    queue = Queue()

    cozmo_thread = cute_cozmo.Cozmo_thread(queue)
    cozmo_thread.daemon = True
    cozmo_thread.start()

    ka = KeyboardApp(cozmo_thread, queue)
    ka.run()
