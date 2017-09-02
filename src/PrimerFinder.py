from OligoAnalyzer import OligoAnalyzer

class PrimerFinder(object):
    def __init__(self, DNA_string, dnaL = 100, pL = 40):
        self.MIN_DNA_LENGTH = dnaL
        self.PRIMER_START_LENGTH = pL
        self.DNA = list(DNA_string)
        self.length = len(self.DNA)
        if (self.length < self.MIN_DNA_LENGTH):
            raise Exception("DNA strand with " + str(self.length) + " base pairs is too short")

        self.bases = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
        self.DNAcomp = list(map(lambda c: self.bases[c], self.DNA))

    def init_amplify(self, start, end):
        self.start = start
        self.end = end

    def init_primers(self):
        fwd_start = self.start - self.PRIMER_START_LENGTH
        if fwd_start < 0:
            fwd_start = self.length + fwd_start
        fwd_end = self.start - 1
        fwd_strand = self.get_substrand(fwd_start, fwd_end, self.DNA)

        # REV points from end to start
        rev_end = (self.end + self.PRIMER_START_LENGTH) % self.length
        rev_start = (self.end + 1) % self.length
        rev_strand = self.get_substrand(rev_start, rev_end, self.DNAcomp)

        self.fwd = Primer(fwd_start, fwd_end, fwd_strand, False)
        self.rev = Primer(rev_start, rev_end, rev_strand, True)

    def init_analyzer(self):
        self.analyzer = OligoAnalyzer()

    def validate_primers(self):


    def get_substrand(self, start, end, strand):
        if start <= end:
            return strand[start:end+1]
        else:
            return strand[start:] + strand[:end+1]


class Primer(object):
    def __init__(self, start, end, strand, rev):
        self.start = start
        self.end = end
        self.strand = strand
        self.rev = rev
        if rev:
            self.tail = (self.start + , self.end)
            self.head = self.start
        else:
            self.tail = self.start
            self.head = self.end

    def __str__(self):
        return "Primer:" + "\ntype:\t" + ("REV" if self.rev else "FWD") + "\nstart:\t" + str(self.start) + "\nend:\t" + str(self.end) + "\nhead:\t" + str(self.head) + "\ntail:\t" + str(self.tail) + "\nsequence:\n " + str(self.strand) + "\n"

if __name__ == "__main__":
    import random

    bases = ['A','C','G','T']
    strand = "".join([random.choice(bases) for _ in range(10)])
    print(strand)
    PF = PrimerFinder(strand)
    PF.init_amplify(8,2)
    PF.init_primers()
    print(PF.fwd)
    print(PF.rev)
