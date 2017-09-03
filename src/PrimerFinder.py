from src.OligoAnalyzer import OligoAnalyzer
from src.Primer import PrimerPair, Primer, PrimerPart, PrimerType, PrimerDirection

class PrimerFinder(object):
    def __init__(self, DNA_string, dnaL = 100, pL = 20): # TODO: ask about better default minimum dnaLength?
        # DNA_string : str
        # dnaL : int
        # pL : int
        self.MIN_DNA_LENGTH = dnaL
        self.PRIMER_START_LENGTH = pL
        self.DNA = DNA_string.upper()
        self.length = len(self.DNA)
        if (self.length < self.MIN_DNA_LENGTH):
            raise Exception("DNA strand with " + str(self.length) + " base pairs is too short")

        self.bases = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

        # store DNA complement TODO: is this still useful?
        self.DNAcomp = "".join([self.bases[c] for c in self.DNA])

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
        insert_fwd = Primer([b, c], [a, b], PrimerDirection.FWD)

        # setup REV for insert:
        insert_rev = Primer([d, e], [e, f], PrimerDirection.REV)

        # setup FWD for backbone:
        backbone_fwd = Primer([e, f], [d, e], PrimerDirection.FWD)

        # setup REV for backbone:
        backbone_rev = Primer([a, b], [b, c], PrimerDirection.REV)

        # organize all primers
        self.insert_primers = PrimerPair(insert_fwd, insert_rev)
        self.backbone_primers = PrimerPair(backbone_fwd, backbone_rev)

    def refine_primers(self):
        if self.insert is None:
            return None # TODO: should this throw error instead?
        self.init_primers()
        self.init_analyzer()


    def validate_primer_pair(self, primer_pair):
        # primer_pair : PrimerPair

        # should only be called from 'refine_primers'

        # TODO: vv For testing purposes ONLY - REMOVE!
        self.init_primers()
        self.init_analyzer()
        # TODO: ^^ For testing purposes ONLY - REMOVE!

        fwd_strand = self.strand(primer_pair.fwd.indices)
        fwd_anneal = self.analyzer.analyze_temp(self.strand(primer_pair.fwd.head.seq))
        fwd_whole = self.analyzer.analyze_temp(fwd_strand)

        rev_strand = self.comp(primer_pair.rev.indices)
        rev_anneal = self.analyzer.analyze_temp(self.comp(primer_pair.rev.head.seq))
        rev_whole = self.analyzer.analyze_temp(rev_strand)

        # Total primer length MUST NOT exceed 60 bp
        valid_length = len(fwd_strand) <= 60 and len(rev_strand) <= 60

        # T anneal of FWD must be 3°C around T anneal of REV
        valid_anneal = abs(fwd_anneal - rev_anneal) <= 3

        # likewise, T whole of FWD must be 3°C around T whole of REV
        valid_whole = abs(fwd_whole - rev_whole) <= 3

        # Temperatures MUST NOT exceed 72°C
        valid_temp = all([t <= 72 for t in (fwd_anneal, fwd_whole, rev_anneal, rev_whole)])

        # Keep track of the “GC content” of the ENTIRE PIECE! Should be between 40%-60%!
        valid_gc = 0.4 <= sum([s.count('G') + s.count('C') for s in (fwd_strand, rev_strand)]) / (len(fwd_strand) + len(rev_strand)) <= 0.6

        # TODO: needs to return what failed so parent function know's what to do
        return all((valid_length, valid_anneal, valid_whole, valid_temp, valid_gc))


    def strand(self, indices):
        return self.DNA[indices[0]:indices[1]]

    def comp(self, indices):
        return self.DNAcomp[indices[0]:indices[1]]

    def __del__(self):
        if not self.analyzer is None:
            del self.analyzer





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
    PF.validate_primer_pair(PF.insert_primers)
