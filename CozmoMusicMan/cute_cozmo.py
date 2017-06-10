import cozmo
import time
import asyncio
import math

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
    def __init__(self, robot: cozmo.robot.Robot):
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
        self.armsDown()

        # we face each direction (center, left and right) hoping to find a cube
        print('Finding cubes')
        self.cubes = list()
        current_note = 0
        for i in range(3):
            self.face_cube(i)
            try:
                cube = self.robot.world.wait_for_observed_light_cube(1)
            except:
                # self.robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                print('no cube detected :(')
                self.face_cube(1)
                return
            
            self.cubes.append(cube)
            current_cube_index = i
            while self.cube_from_note(current_note) is i and current_note < len(self.notes):
                print('preparing to play', current_note)
                self.play(current_note)
                current_note += 1
            #print(current_cube, 'is not', i)
                
        self.face_cube(1)
        for cube in self.cubes:
            cube.set_lights(cozmo.lights.off_light)

    # quickly shove the lift down
    def hit(self, wait=True, parallel=False):
        self.robot.set_lift_height(1, 500, 20).wait_for_completed()
        action = self.robot.set_lift_height(0, 500, 20,in_parallel=parallel)
        if wait:
            action.wait_for_completed()
        return action

    def armsUp(self, speed=5):
        self.robot.set_lift_height(1).wait_for_completed()

    def armsDown(self, speed=5):
        self.robot.set_lift_height(0).wait_for_completed()

    def switch_off_cubes(self):
        for c in self.cubes:
            c.set_lights(cozmo.lights.off_light)

    def cube_from_note(self, note):
        nb_notes = len(self.notes)
        cube_index = 0
        if nb_notes % 3 == 1:
            if note+1 < nb_notes / 3:
                cube_index = 0
            elif note <= nb_notes*2/3:
                cube_index = 1
            else:
                cube_index = 2
        else:
            if note < nb_notes / 3:
                cube_index = 0
            elif note+1 <= nb_notes*2/3:
                cube_index = 1
            else:
                cube_index = 2
        return cube_index

    # light a certain cube with the correct color
    def light_led(self, led_index):
        nb_notes = len(self.notes)
        light = self.lights[led_index]
        if len(self.notes) == 3:
            self.cubes[led_index].set_lights(light)
        else:
            cube_index = self.cube_from_note(led_index)
            print('cube_index =', cube_index)
            self.cubes[cube_index].set_lights(light)
        self.robot.set_all_backpack_lights(light)

    # play a note, or a series of notes
    def play(self, toPlay, incremental=False):
        if type(toPlay) == int:
            noteToPlay = None
            if toPlay >= 0 and toPlay < len(self.notes):
                noteToPlay = self.notes[toPlay]
            else:
                noteToPlay = -1
            self.notePlaying = noteToPlay
            self.face_note(toPlay)
            while True: # hold on to your butts, we're gonna do a "do ... while" in python !
                action = self.hit(False,True)
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
        #empty the queue
        print('before :', q)
        try:
            while q.get_nowait() is not None:
                pass
        except:
            pass
        print('after :', q)

        #pass # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True
        print('waiting for note', note)
            # code to receive note from MainThread
        print('pre get')
        try:
            playedNote = q.get(timeout=timeout)
        except:
            return False
        print('post get')
        return playedNote == note
        # if playedNote == note:
        #     return True
        # return False


    def face_cube(self, i, wait=True):
        angle = (self.facing - i) * 0.5
        action = self.robot.turn_in_place(Angle((self.facing - i)*0.5))
        if wait:
            action.wait_for_completed()
        self.facing = i
        return action


    # make Cozmo face a certain direction
    def face_note(self, i, wait=True):
        cubeToFace = self.cube_from_note(i)
        print('note',i,'-> cube',cubeToFace)
        return self.face_cube(cubeToFace,wait)

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
    # cute.setup()
    # KnockOverEyes : when user is playing music
    # MajorWin : vas-y, joue !
    # MemoryMatchPlayerLoseHandSolo : quand user se plante
    #cute.robot.play_anim_trigger(cozmo.anim.Triggers.MemoryMatchPlayerWinHandSolo).wait_for_completed()
    cute.robot.play_anim_trigger(cozmo.anim.Triggers.OnSpeedtapGameCozmoWinLowIntensity ).wait_for_completed()
    # cute.play(0)
    # if cute.wait_for_note(0):
    #     cute.robot.say_text('bravo').wait_for_completed()
    # else:
    #     cute.robot.say_text('caca').wait_for_completed()

def setup_pygame():
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.update()

class Cozmo_thread(threading.Thread):
    def __init__(self, q1: Queue):
        super().__init__()
        global q
        q = q1

    def run(self):
        cozmo.run_program(cozmo_program)

