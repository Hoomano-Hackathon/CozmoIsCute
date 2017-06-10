import cozmo
import time
import asyncio

from enum import Enum
from cozmo.util import degrees, distance_mm, Angle

from sound_player import Sound
import pygame

'''
Goes in the trigonometric way
'''
class Dir(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

class CuteCozmo:

    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot
        self.facing = 1
        self.notes = [20,22,24]
        self.colors = [
            cozmo.lights.red_light,
            cozmo.lights.green_light,
            cozmo.lights.blue_light
        ]
    
    def setup(self):
        self.robot.world.connect_to_cubes()
        self.robot.set_head_angle(Angle(0)).wait_for_completed()

        
        self.cubes = list()
        for i in range(3):
            self.face(i)
            color = self.colors[i]
            try:
                cube = self.robot.world.wait_for_observed_light_cube(1)
            except:
                # self.robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                print('no cube detected :(')
                self.face(1)
                return
            self.cubes.append(cube)
            cube.set_lights(color)
            self.play(i)
            cube.set_lights(color)

        self.face(1)
        for cube in self.cubes:
            cube.set_lights(cozmo.lights.off_light)

    def light_cube(self, cube_index):
        self.cubes[cube_index].set_lights(self.colors[cube_index])

    def play(self, toPlay, incremental=False):
        if type(toPlay) == int:
            noteToPlay = None
            if toPlay >= 0 and toPlay < len(self.notes):
                noteToPlay = self.notes[toPlay]
            else:
                noteToPlay = -1
            self.notePlaying = noteToPlay
            while True: # hold on to your butts, we're gonna do a "do ... while" in python !
                self.light_cube(toPlay)
                sound.play(noteToPlay)
                self.cubes[toPlay].set_lights(cozmo.lights.off_light)
                if not incremental or self.wait_for_note(noteToPlay):
                    break
        elif type(toPlay) == list:
            for note in toPlay:
                self.play(note)
    
    def wait_for_note(self, note):
        pass # TODO STUART

    def face(self, i):
        self.robot.turn_in_place(Angle(self.facing - i)).wait_for_completed()
        self.facing = i

    def lift_a_cube(self):
        look_around = self.robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cube = None
        try:
            cube = self.robot.world.wait_for_observed_light_cube(timeout=30)
            print("Found cube: %s" % cube)
        except asyncio.TimeoutError:
            print("Didn't find a cube")
            return
        finally:
            # whether we find it or not, we want to stop the behavior
            look_around.stop()
        #self.robot.go_to_object(cube, distance_mm(70.0)).wait_for_completed()
        self.robot.pickup_object(cube).wait_for_completed()

    def hit(self):
        self.robot.set_lift_height(0,duration=0.15).wait_for_completed()

    def armsUp(self, speed=5):
        self.robot.set_lift_height(1).wait_for_completed()
        
    def armsDown(self, speed=5):
        self.robot.set_lift_height(0).wait_for_completed()

def cozmo_program(robot: cozmo.robot.Robot):
    cute = CuteCozmo(robot)
    cute.setup()
    cute.play([0,0,0,1,2,-1,1,0,2,1,1,0])

def setup_pygame():
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.update()

sound = Sound()
setup_pygame()
cozmo.run_program(cozmo_program)
