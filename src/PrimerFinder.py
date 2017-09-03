from src.OligoAnalyzer import OligoAnalyzer
from src.Primer import PrimerPair, Primer, PrimerPart, PrimerType, PrimerDirection

class PrimerFinder(object):
    def __init__(self, DNA_string, dnaL = 100, pL = 20): # TODO: ask about better default minimum dnaLength?
        # DNA_string : str
        # dnaL : int
        # pL : int
        self.MIN_DNA_LENGTH = dnaL
        self.PRIMER_START_LENGTH = pL
        self.DNA = DNA_string
        self.length = len(self.DNA)
        if (self.length < self.MIN_DNA_LENGTH):
            raise Exception("DNA strand with " + str(self.length) + " base pairs is too short")

        self.bases = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

        # store DNA complement TODO: is this still useful?
        self.DNAcomp = [self.bases[c] for c in self.DNA]

        # initialize the insert:
        self.start = None
        self.end = None

    def init_analyzer(self):
        self.analyzer = OligoAnalyzer()

    def init_insert(self, insert):
        try:
            start = self.DNA.index(insert)
        except ValueError:
            print("The given sub-strand not found in DNA string.")
            return

        end = start + len(insert)
        self.start = start
        self.end = end

    def init_primers(self):
        #       a      b       c                d        e        f
        #            start                              end
        a,b,c = self.start - self.PRIMER_START_LENGTH, self.start, self.start + self.PRIMER_START_LENGTH
        d,e,f = self.end - self.PRIMER_START_LENGTH, self.end, self.end + self.PRIMER_START_LENGTH

        # setup FWD for insert:
        head = PrimerPart([b, c], PrimerType.HEAD)
        tail = PrimerPart([a, b], PrimerType.TAIL)
        insert_fwd = Primer(head, tail, PrimerDirection.FWD)

        # setup REV for insert:
        head = PrimerPart([d, e], PrimerType.HEAD)
        tail = PrimerPart([e, f], PrimerType.TAIL)
        insert_rev = Primer(head, tail, PrimerDirection.REV)

        # setup FWD for backbone:
        head = PrimerPart([e, f], PrimerType.HEAD)
        tail = PrimerPart([d, e], PrimerType.TAIL)
        backbone_fwd = Primer(head, tail, PrimerDirection.FWD)

        # setup REV for backbone:
        head = PrimerPart([a, b], PrimerType.HEAD)
        tail = PrimerPair([b, c], PrimerType.TAIL)
        backbone_rev = Primer(head, tail, PrimerDirection.REV)

        # organize all primers
        self.insert_primers = PrimerPair(insert_fwd, insert_rev)
        self.backbone_primers = PrimerPair(backbone_fwd, backbone_rev)

    def refine_primers(self):
        if self.insert is None:
            return None # TODO: should this throw error instead?
        self.init_primers()
        self.init_analyzer()




# class Primer(object):
#     def __init__(self, start, end, strand, rev):
#         self.start = start
#         self.end = end
#         self.strand = strand
#         self.rev = rev
#         if rev:
#             self.tail = (self.start + , self.end)
#             self.head = self.start
#         else:
#             self.tail = self.start
#             self.head = self.end
#
#     def __str__(self):
#         return "Primer:" + "\ntype:\t" + ("REV" if self.rev else "FWD") + "\nstart:\t" + str(self.start) + "\nend:\t" + str(self.end) + "\nhead:\t" + str(self.head) + "\ntail:\t" + str(self.tail) + "\nsequence:\n " + str(self.strand) + "\n"

if __name__ == "__main__":
    import random

    bases = ['A','C','G','T']
    strand = "".join([random.choice(bases) for _ in range(1000)])
    print(strand)
    PF = PrimerFinder(strand)
    PF.init_insert(strand[500:550])
    PF.init_primers()
    print(PF.insert_primers)
    print(PF.backbone_primers)
