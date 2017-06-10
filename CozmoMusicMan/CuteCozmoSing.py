import cozmo
from cozmo.util import Angle
import asyncio
from sound_player import Sound


class _CuteCozmoSing:
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
        self.lights = self.setup_color()
        self.cubes = None
        self.setup()

    def setup_color(self):
        lights = []
        for t in _CuteCozmoSing.color_rgb:
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
        print('hitting')
        self.robot.set_lift_height(1, 500, 20).wait_for_completed()
        return self.robot.set_lift_height(0, 500, 20)

    def armsUp(self, speed=5):
        self.robot.set_lift_height(1).wait_for_completed()

    def armsDown(self, speed=5):
        self.robot.set_lift_height(0).wait_for_completed()

    # light a certain cube with the correct color
    def light_cube(self, cube_index):
        self.cubes[cube_index].set_lights(self.lights[cube_index])

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


class CozmoSingleton:
    singleton = None

    def __init__(self, robot: cozmo.robot.Robot):
        if not CozmoSingleton.singleton:
            CozmoSingleton.singleton = _CuteCozmoSing(robot)
        self.robot = CozmoSingleton.singleton
        self.sound = CozmoSingleton.singleton.sound
        self.facing = CozmoSingleton.singleton.facing
        self.lights = CozmoSingleton.singleton.lights
        self.cubes = CozmoSingleton.singleton.cubes

    def setup_color(self):
        return CozmoSingleton.singleton.setup_color()

    def setup(self):
        CozmoSingleton.singleton.setup()

    # quickly shove the lift down
    def hit(self):
        return CozmoSingleton.singleton.hit()

    def armsUp(self, speed=5):
        CozmoSingleton.singleton.armsUp()

    def armsDown(self, speed=5):
        CozmoSingleton.singleton.armsDown()

    # light a certain cube with the correct color
    def light_cube(self, cube_index):
        CozmoSingleton.singleton.light_cube(cube_index)

    # make Cozmo face a certain direction
    def face(self, i):
        CozmoSingleton.singleton.face(i)

    def lift_a_cube(self):
        CozmoSingleton.singleton.lift_a_cube()

