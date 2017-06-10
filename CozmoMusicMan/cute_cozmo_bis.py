import cozmo
import time
import asyncio
from cozmo.util import degrees, distance_mm, Angle

from sound_player import Sound
import pygame
import threading
from Notes import Notes


class CuteCozmo:

    color_rgb = [
           (255, 0, 0),
           (0, 255, 0),
           (0, 0, 255),
           (255, 255, 0),
           (255, 0, 255),
           (0, 255, 255),
           (255, 255, 255),
           (255, 0, 0)
       ]

    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot
        self.sound = Sound()
        self.facing = 1
        # self.notes = [20, 22, 24]
        self.lights = self.setup_color()
        self.notes = None
        self.cubes = None
        self.setup()
        self.notes = Notes(self.sound, self.cubes, self.lights, simple_mode=False)

    def setup_color(self):
        lights = []
        for t in CuteCozmo.color_rgb:
            lights.append(cozmo.lights.Light(cozmo.lights.Color(rgb=t)))
        return lights

    def setup(self):
        # reconnect to the cubes in case we lost them
        self.robot.world.connect_to_cubes()
        # make the head horizontal
        self.robot.set_head_angle(Angle(0)).wait_for_completed()

        # we face each direction (center, left and right) hoping to find a cube
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
            # self.play_note(i)
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

    # light a certain cube with the correct color
    def light_cube(self, cube_index):
        self.cubes[cube_index].set_lights(self.lights[cube_index])

    def play_partition(self, partition: [int]):
        for note in partition:
            self.play_note(note)

    def play_note(self, note: int):
        if self.notes is not None:
            action = self.hit()
            self.notes.play_complete_note(note)
            action.wait_for_completed()
        else:
            print('no notes in instance !')

    def wait_for_note(self, note, timeout=5):
        pass  # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True

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
    cute.hit().wait_for_completed()
    cute.play_partition([0, 0, 0, 1, 2, -1, 1, 0, 2, 1, 1, 0])
    # cute.play_partition([20, 20, 20, 22, 24, -1, 22, 20, 24, 22, 22, 20])


def setup_pygame():
    pygame.init()
    windowSurface = pygame.display.set_mode((500, 400), 0, 32)
    pygame.display.update()


class Cozmo_thread(threading.Thread):
    def run(self):
        cozmo.run_program(cozmo_program)
