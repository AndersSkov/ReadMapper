import suffix_array as sa
import bwt
import approx as app

input = b'googol$'
# baabaabac$
# gatgcgagagatg$
input_search = "lol"

edits = "AACTTTCTGAA"
testString1 = "TTAAAAAATTTCT-AACAACA"
testString2 = "TGGAAAA-TTTCTGGAATGGAT"

test = b'gatgcgagagatg$'
test_search = "gaga"


#print("naive implementation of suffix array")
sa.naive(input)

#print("SA-IS")
SA = sa.SA_IS(input, 256)
print("SA-IS\n", SA)

#print("skew implementation of suffix array")
#sa.skew(input)

#print("naive implementation of bwt")
our_bwt = bwt.naive(input.decode())
rev_bwt = bwt.naive(input.decode()[::-1])
print("BWT\n", our_bwt)
print("BWT of REV INPUT\n", rev_bwt)

#print("naive implementation of bwt_inverse")
#bwt.naive_inverse(inverse)


c = bwt.c_tabel(input)
print("C TABLE \n", c)


o = bwt.o_table(list(c.keys()), our_bwt)
ro = bwt.o_table(list(c.keys()), rev_bwt)
print("O TABLE\n", o)
print("RO TABLE\n", ro)

print("EXACT SEARCH")
i1, i2 = bwt.bwt_search(c, o, input_search)
for i in range(i1, i2):
    print(SA[i])

print("APPROX SEARCH")
d = app.d_table(input_search, c, ro, SA)
print("D TABLE\n", d)


def read_fasta_file(filename):
    """
    Reads the given FASTA file f and returns a dictionary of sequences.

    Lines starting with ';' in the FASTA file are ignored.
    """
    sequences_lines = {}
    current_sequence_lines = None
    with open(filename) as fp:
        for line in fp:
            line = line.strip()
            if line.startswith(';') or not line:
                continue
            if line.startswith('>'):
                sequence_name = line.lstrip('>')
                current_sequence_lines = []
                sequences_lines[sequence_name] = current_sequence_lines
            else:
                if current_sequence_lines is not None:
                    current_sequence_lines.append(line)
    sequences = {}
    for name, lines in sequences_lines.items():
        sequences[name] = ''.join(lines)
    return sequences

