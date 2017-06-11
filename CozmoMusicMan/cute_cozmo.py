import cozmo
from cozmo.util import Angle

import time
import csv
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

def mini_jeu_lire_melodie():
    melodie = list()
    with open('partition.txt') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            for item in row:
                if item is '' or item.isspace():
                    break
                # print('note :', item)
                melodie.append(int(item))
    return melodie


def mini_jeu_jouer_melodie(cute: CuteCozmo, melodie = None, taille_groupe = 4):
    if melodie == None:
        melodie = mini_jeu_lire_melodie()
    # clear cube hit before
    for cube in cute.cubes:
        cube.last_tapped_time = None

    robot = cute.robot
    # jouer mélodie si complexe
    # if len(melodie) >= taille_groupe: # TODO remettre, c'était pour la démo
    #     cute.play_partition(melodie)
        # animation "ok fin de démo"
        robot.play_anim('anim_meetcozmo_sayname_02').wait_for_completed()
        cute.face_cube(1)
    user_succeded = False
    while not user_succeded:
        print('start while')
        # check if user tapped cube
        for cube in cute.cubes:
            #print('last tapped :', cube.last_tapped_time)
            if cube.last_tapped_time is not None:
                print(cube.last_tapped_time)
                for c in cute.cubes:
                    cube.last_tapped_time = None
                mini_jeu_enregistrer_melodie(cute)
                return
        print('no cube tap detected - proceeding')
        taille_ensemble = 0
        while taille_ensemble <= len(melodie):
            cute.play_partition(melodie[:taille_ensemble])

            robot.play_anim('anim_rtpmemorymatch_request_02').wait_for_completed() # à toi
            cute.face_cube(1)

            if not cute.wait_for_partition(melodie[:taille_ensemble]):
                print('user planted himself')
                robot.play_anim('anim_cozmosays_badword_01').wait_for_completed()
                cute.face_cube(1)
                break
            elif taille_ensemble == len(melodie):
                print('user a reussi')
                robot.play_anim('anim_meetcozmo_sayname_02').wait_for_completed()
                cute.face_cube(1)
                user_succeded = True
                break
            elif len(melodie) - taille_ensemble <= taille_groupe:
                taille_ensemble = len(melodie)
            else:
                taille_ensemble += taille_groupe

def mini_jeu_enregistrer_melodie(cute: CuteCozmo):
    print('saving a melody')
    
    global q
    cute.robot.play_anim('anim_explorer_huh_01').wait_for_completed() # curious
    cute.face_cube(1)
    # empty queue
    while not q.empty():
        try:
            q.get(False)
        except Empty:
            continue
        q.task_done()
    # TODO make cubes blink
    blink_light = cozmo.lights.Light(cozmo.lights.Color(rgb=(255,255,255)), cozmo.lights.off, off_period_ms=250, transition_off_period_ms=50, transition_on_period_ms=50)
    for cube in cute.cubes:
        cube.set_lights(blink_light)
    # wait while not tap
    tapped = False
    while not tapped:
        print('waiting for tap')
        for cube in cute.cubes:
            if cube.last_tapped_time is not None:
                tapped = True
        if not tapped:
            time.sleep(1)
    
    with open('partition.txt', 'w') as f:
        while True:
            try:
                note = q.get(False)
            except:
                break
            f.write(str(note) + ' ')
            q.task_done()
    # make cubes switch off
    for cube in cute.cubes:
        cube.set_lights(cozmo.lights.off_light)

def cozmo_program(robot: cozmo.robot.Robot):
    # dire_bonjour+setup
    robot.play_anim('anim_freeplay_reacttoface_like_01').wait_for_completed()
    
    cute = CuteCozmo(robot)
    cute.face_cube(1)
    # demo gamme
    for i in range(8):
        cute.play_note(i)
    
    # Animation content, je t'invite a continuer
    robot.play_anim('anim_fistbump_success_01').wait_for_completed()
    cute.face_cube(1)
    #Partie jouer mélodie simple
    melodie = [1,4,7]
    print('playing simple melody')
    mini_jeu_jouer_melodie(cute, melodie)
    mini_jeu_enregistrer_melodie(cute)
    robot.play_anim('anim_hiking_observe_01').wait_for_completed()
    mini_jeu_jouer_melodie(cute)

    robot.play_anim('anim_freeplay_reacttoface_like_01').wait_for_completed()
    robot.turn_in_place(Angle(degrees=180)).wait_for_completed()
    robot.drive_wheels(500, 500)
    time.sleep(5)


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
