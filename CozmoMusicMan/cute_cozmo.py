import cozmo
from cozmo.util import Angle

from enum import Enum
import pygame
import threading
from queue import Queue
from CuteCozmoSing import CozmoSingleton
from Notes import Notes

'''
Goes in the trigonometric way
'''
class Dir(Enum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3


class CuteCozmo(CozmoSingleton):
    def __init__(self, robot: cozmo.robot.Robot):
        CozmoSingleton.__init__(self, robot)
        self.notes = Notes(robot, simple_mode=False)

    # TODO : tester et verifier...
    def wait_and_learn(self):
        start = self.double_tap()  # on attend que le double tap soit fait (renvoie True ou False si delai trop long)
        if not start:  # si il n'y a pas eu de double tap -> possibilite de mettre une animation
            return
        global q
        # empty the queue
        try:
            while q.get_nowait() is not None:
                pass
        except:
            pass

        partition = []
        next_note = self.learn_next_note()
        while next_note >= 0:  # tant qu'on a des notes jouees avant 20s d'intervalle
            partition.append(next_note)
        return partition



    def learn_next_note(self):
        try:
            playedNote = q.get(timeout=20)  # on attend 20s max entre deux notes
        except:  # si les 20s sont depassees
            return -1
        return playedNote

    def play_partition(self, partition: [int]):
        for note in partition:
            self.play_note(note)

    def play_note(self, note: int):
        if self.notes is not None:
            
            # action = self.hit()
            self.notes.play_complete_note(note)
            # action.wait_for_completed()
            # cube.set_lights(cozmo.lights.off_light)
        else:
            print('no notes in instance !')


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

    def wait_for_partition(self, partition: [int], timeout=5):
        for note in partition:
            if not self.wait_for_note(note):
                return False
        return True

    def wait_for_note(self, note, timeout=5):
        if note == -1:
            return True
        global q
        # empty the queue
        print('before :', q)
        try:
            while q.get_nowait() is not None:
                pass
        except:
            pass
        print('after :', q)

        # pass # TODO STUART
        # we wait for the correct signal
        # if the user inputs the wrong note, or if no note is given in $timeout seconds, return False
        # otherwise, return True
        print('waiting for note', note)
        # code to receive note from MainThread
        #print('pre get')
        try:
            playedNote = q.get(timeout=timeout)
        except:
            return False
        #print('post get')
        return playedNote == note
        # if playedNote == note:
        #     return True
        # return False


def cozmo_program(robot: cozmo.robot.Robot):
    # dire_bonjour+s etup
    cute = CuteCozmo(robot)

    # apprentissage d'une partion et rejouer
    part = cute.wait_and_learn()  # apprend une partition
    cute.play_partition(part)  # la rejoue

    # demo gamme
    for i in range(8):
        cute.play_note(i)
    
    # TODO Animation content, je t'invite a continuer
    #Partie jouer mélodie simple
    melodie = [1,4,7]
    clair_de_lune = [0,0,0,1,2,1,0,2,1,1,0] # points bonus si tu devines la mélodie à partir des ints

    user_succeded = False
    while not user_succeded:
        cute.play_partition(melodie)
        # TODO animation "à toi"
        user_succeded = cute.wait_for_partition(melodie)
        if user_succeded:
            # TODO animation "bravo"
            break
        else:
            pass
            # TODO animation "tocard"
    
    # jouer mélodie complexe
    cute.play_partition(clair_de_lune)
    # TODO animation "ok fin de démo"
    user_succeded = False
    taille_groupe = 4
    while not user_succeded:
        taille_ensemble = taille_groupe
        while taille_ensemble <= len(clair_de_lune):
            cute.play_partition(clair_de_lune[:taille_ensemble])
            # TODO animation "à toi"
            if not cute.wait_for_partition(clair_de_lune[:taille_ensemble]):
                break
            elif taille_ensemble == len(clair_de_lune):
                user_succeded = True
                break
            elif len(clair_de_lune) - taille_ensemble <= taille_groupe:
                taille_ensemble = len(clair_de_lune)
            else:
                taille_ensemble += taille_groupe


            
    # if cute.wait_for_note(1):
    #     print('content !')
    #     cute.robot.play_anim_trigger(cozmo.anim.Triggers.OnSpeedtapGameCozmoWinLowIntensity).wait_for_completed()
    # else:
    #     print('fâché !')
    #     cute.robot.play_anim_trigger(cozmo.anim.Triggers.MemoryMatchPlayerLoseHandSolo).wait_for_completed()
    # cute.play_partition([0, 1, 2, 3, 4, 5, 6, 7])
    # cute.play_partition([0, 0, 0, 1, 2, -1, 1, 0, 2, 1, 1, 0])


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
