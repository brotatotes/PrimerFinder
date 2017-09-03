from enum import Enum

class PrimerType(Enum):
    HEAD = "HEAD"
    TAIL = "TAIL"

class PrimerDirection(Enum):
    FWD = "FWD"
    REV = "REV"

class PrimerPart(object):
    def __init__(self, DNA_indices, type):
        # type : PrimerType.str
        # seq : [int, int]
        self.type = type
        self.seq = DNA_indices

    def __repr__(self):
        return self.type.name + ": " + str(self.seq)

class Primer(object):
    def __init__(self, head, tail, direction):
        # head : [int, int]
        # tail : [int, int]
        # direction : PrimerDirection.int

        # head and tail should always be in order from 5' -> 3'
        self.head = PrimerPart(head, PrimerType.HEAD)
        self.tail = PrimerPart(tail, PrimerType.TAIL)
        self.direction = direction
        if self.direction is PrimerDirection.FWD:
            self.indices = self.tail.seq[0], self.head.seq[1]
        else:
            self.indices = self.head.seq[0], self.tail.seq[1]

    def __repr__(self):
        return self.direction.name + " Primer: " + "\n\t" + str(self.head) + "\n\t" + str(self.tail)


class PrimerPair(object):
    def __init__(self, fwd, rev):
        # fwd : Primer
        # rev : Primer
        self.fwd = fwd
        self.rev = rev

    def __repr__(self):
        return "PrimerPair:\n" + str(self.fwd) + "\n" + str(self.rev) + "\n"