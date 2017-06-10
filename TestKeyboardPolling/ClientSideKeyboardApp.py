import pygame, sys, os, time
from pygame.locals import *
from sound_player import Sound

# set up pygame
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.init()

dir_path = os.path.dirname(os.path.realpath(__file__))

print(dir_path)


rect_dict = {}

# set up the window
windowSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Cozmo is cute')

# set up the colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# set up fonts
basicFont = pygame.font.SysFont(None, 48)

# draw the white background onto the surface
windowSurface.fill(WHITE)

letters = "zqsdfg"

# draw the "keys" on the canvas
for num in range(0,6):
    rect = pygame.draw.rect(windowSurface, BLUE, (20+60*num, 20, 40, 40))
    rect_dict[letters[num]] = [rect, num]

"""rect = pygame.draw.rect(windowSurface, BLUE, (80, 20, 40, 40))
rect_dict["q"] = [rect, 1]

rect = pygame.draw.rect(windowSurface, BLUE, (140, 20, 40, 40))
rect_dict["s"] = [rect, 2]"""


# pygame.draw.rect(windowSurface, BLUE, (rect + 20, rect + 20, 40, 40))
# get a pixel array of the surface
pixArray = pygame.PixelArray(windowSurface)
pixArray[480][380] = RED
del pixArray

# draw the window onto the screen
pygame.display.update()

soundPlayer = Sound()

# run the game loop
while True:
    # Reset all rect colors
    for key in rect_dict:
        windowSurface.fill(BLUE, rect_dict[key][0])

    # Check current key presses
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        for (key,toinput) in [(pygame.K_w,"z"),(pygame.K_a,"q"),(pygame.K_s,"s"),(pygame.K_d,"d"),(pygame.K_f,"f")]:
            if pressed[key]:
                rectProp = rect_dict[toinput]
                windowSurface.fill(RED, rectProp[0])
                soundPlayer.play(rectProp[1], False)
                break
        if pressed[pygame.K_p]:
            pygame.quit()
            sys.exit()

        pygame.display.update()
