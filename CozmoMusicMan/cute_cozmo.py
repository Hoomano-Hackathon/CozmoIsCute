import cozmo
import time
import asyncio

from enum import Enum

from cozmo.util import degrees, distance_mm, Angle

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
    
    def setup(self):
        angles = [-1,2,-1]
        colors = [cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.blue_light]
        self.cubes = list()
        for i in range(3):
            self.face(i)
            color = colors[i]
            try:
                cube = self.robot.world.wait_for_observed_light_cube(1)
            except:
                # self.robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession).wait_for_completed()
                print('no cube detected')
                return
            self.cubes.append(cube)
            cube.set_lights(color)
            #self.robot.turn_in_place(Angle(a)).wait_for_completed()
        
        self.face(1)
    
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

cozmo.run_program(cozmo_program)
