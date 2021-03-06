from ..sound_player import Sound


class Note:

    def __init__(self, note: int, duration: int=2):
        self.note = note
        self.duration = duration

    def __str__(self):
        return '[', self.note, ' ,', self.duration, ']'

    def __repr__(self):
        return '[' + str(self.note) + ' ,' + str(self.duration) + ']'


class Partition:

    def __init__(self, speed: int=60, notes: []=None, note_int: [int]=None):
        self.speed = speed
        self.notes = None
        self.sound = Sound()
        if notes:
            self.notes = notes
            print(self.notes)
        elif note_int:
            self.notes = Partition.pationning_with_int(note_int)

    def pationning_with_int(cls, note_int: [int]):
        part = []
        for n in note_int:
            part.append(Note(n))
        return part

    def play_part(self):
        for n in self.notes:
            self.sound.play(n.note, (n.duration * 60) / (self.speed))

    @staticmethod
    def partitionning(self, tab_part: [[int]]):
        part = []
        for t in tab_part:
            if len(t) == 2:
                part.append(Note(t[0], t[1]))
        return part

tab = Partition.partitionning(Partition, [[0, 1],
                               [0, 1],
                               [0, 1],
                               [1, 1],
                               [2, 2],
                               [1, 1],
                               [0, 1],
                               [2, 1],
                               [1, 1],
                               [1, 1],
                               [0, 1]])

p = Partition(80, notes=tab)
p.play_part()