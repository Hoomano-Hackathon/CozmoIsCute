import cozmo
import time

#def hit(robot: cozmo.robot.Robot, speed=5):

class CuteCozmo:
    def __init__(self, robot: cozmo.robot.Robot):
        self.robot = robot

    def hit(self):
        self.robot.set_lift_height(0,duration=0.15).wait_for_completed()

    def armsUp(self, speed=5):
        self.robot.set_lift_height(1).wait_for_completed()
        
    def armsDown(self, speed=5):
        self.robot.set_lift_height(0).wait_for_completed()
        


def cozmo_program(robot: cozmo.robot.Robot):
    cute = CuteCozmo(robot)
    for i in range(2):
        cute.armsUp()
        cute.hit()


cozmo.run_program(cozmo_program)
