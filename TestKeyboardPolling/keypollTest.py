import pygame, sys, os, time
from pygame.locals import *

# set up pygame
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)

s = pygame.mixer.Sound(dir_path + "\\test.wav")


"""rect_dict = {}

# set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Cozmo is cute')

# set up the colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# draw the white background onto the surface
windowSurface.fill(WHITE)

# draw the text's background rectangle onto the surface
rect = pygame.draw.rect(windowSurface, BLUE, (20, 20, 40, 40))
rect_dict["k"] = rect
#pygame.draw.rect(windowSurface, BLUE, (rect + 20, rect + 20, 40, 40))
# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = RED
del pixArray

# draw the window onto the screen
pygame.display.update()"""

s.play()
time.sleep(5)

# run the game loop
"""while True:
    windowSurface.fill(BLUE, rect)
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            print("w is pressed")
            windowSurface.fill(RED, rect_dict["k"])
            s.play()
        elif pressed[pygame.K_s]:
            print("s is pressed")
        elif pressed[pygame.K_o]:
            pygame.quit()
            sys.exit()

        pygame.display.update()
"""