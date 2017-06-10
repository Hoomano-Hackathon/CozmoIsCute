import cozmo
import time
import asyncio

from enum import Enum
from cozmo.util import degrees, distance_mm, Angle

from sound_player import Sound
import pygame
import threading
from queue import Queue

q = None

'''
Goes in the trigonometric way
'''
class Dir(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

class CuteCozmo:
    def __init__(self, robot: cozmo.robot.Robot, q: Queue):
        self.q = q
        self.robot = robot
        self.sound = Sound()
        self.facing = 1
        self.notes = range(8) # [20,22,24,26,28,30,32]
        self.color = [
            (255,0,0),
            (0,255,0),
            (0,0,255),
            (255,255,0),
            (255,0,255),
            (0,255,255),
            (255,255,255),
            (255,0,0)
        ]
        self.lights = []
        for c in self.color:
            self.lights.append(cozmo.lights.Light(cozmo.lights.Color(rgb=c)))
    
    def setup(self):
        # reconnect to the cubes in case we lost them
        self.robot.world.connect_to_cubes()
        # make the head horizontal
        self.robot.set_head_angle(Angle(0)).wait_for_completed()

        # we face each direction (center, left and right) hoping to find a cube
        print('Finding cubes')
        self.cubes = list()
        for i in range(3):
            self.face(i)
            color = self.lights[i]
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

    # quickly shove the lift down
    def hit(self):
        self.robot.set_lift_height(1, 500, 20).wait_for_completed()
        return self.robot.set_lift_height(0, 500, 20)

    def armsUp(self, speed=5):
        self.robot.set_lift_height(1).wait_for_completed()

    def armsDown(self, speed=5):
        self.robot.set_lift_height(0).wait_for_completed()

    def switch_off_cubes(self):
        for c in self.cubes:
            c.set_lights(cozmo.lights.off_light)

    # light a certain cube with the correct color
    def light_led(self, led_index):
        nb_notes = len(self.notes)
        if len(self.notes) == 3:
            self.cubes[led_index].set_lights(self.lights[led_index])
        else:
            cube_index = 0
            if nb_notes % 3 == 1:
                if led_index+1 < nb_notes / 3:
                    cube_index = 0
                elif led_index <= nb_notes*2/3:
                    cube_index = 1
                else:
                    cube_index = 2
            light = self.lights[led_index]
            self.cubes[cube_index].set_lights(light)

    # play a note, or a series of notes
    def play(self, toPlay, incremental=False):
        if type(toPlay) == int:
            noteToPlay = None
            if toPlay >= 0 and toPlay < len(self.notes):
                noteToPlay = self.notes[toPlay]
            else:
                noteToPlay = -1
            self.notePlaying = noteToPlay
            while True: # hold on to your butts, we're gonna do a "do ... while" in python !
                action = self.hit()
                self.switch_off_cubes()
                self.light_led(toPlay)
                print('note :', toPlay)
                self.sound.play(noteToPlay, False)
                action.wait_for_completed()
                #self.cubes[toPlay].set_lights(cozmo.lights.off_light)
                self.light_led(toPlay)
                if not incremental or self.wait_for_note(noteToPlay):
                    break
        elif type(toPlay) == list:
            for note in toPlay:
                self.play(note)
    
    def wait_for_note(self, note, timeout=5):
        global q
        #pass # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True
        for tick in range(0, timeout):
            # code to receive note from MainThread
            playedNote = q.get()
            if(playedNote == note):
                return True
            time.sleep(1)

        return False


    # make Cozmo face a certain direction
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


def cozmo_program(robot: cozmo.robot.Robot):
    cute = CuteCozmo(robot)
    cute.setup()
    cute.hit().wait_for_completed()
    #cute.play([0,0,0,1,2,-1,1,0,2,1,1,0])
    for i in range(len(cute.notes)):
        cute.play(i)
    for i in range(len(cute.notes)):
        cute.play(len(cute.notes)-1-i)

def setup_pygame():
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.update()

class Cozmo_thread(threading.Thread):
    def __init__(self, q1: Queue):
        global q
        q = q1

    def run(self):
        cozmo.run_program(cozmo_program)

