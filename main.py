import suffix_array as sa
import bwt
import approx as app

input = b'mississippi$'
# baabaabac$
edits =  ""

print("naive implementation of suffix array")
sa.naive(input)

#print("skew implementation of suffix array")
#sa.skew(input)

#print("naive implementation of bwt")
#inverse = bwt.naive(input)

#print("naive implementation of bwt_inverse")
#bwt.naive_inverse(inverse)

print("SA-IS")
SA = sa.SA_IS(input, 256)
print(SA)



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

