import suffix_array as sa
import bwt
import approx as app

input = b"mmiissiissiippii$"
# baabaabac$
# gatgcgagagatg$
# googol$
input_search = "misss"


ExactSearch = False


sa.naive(input)

SA = sa.SA_IS(input, 256)
print("SA-IS\n", SA)

# Det er temmeligt dumt at bruge en O(n² log n) algoritme
# her, når I jo har et suffix array. Lad være med det!
# Har I tested at I kan bygge BWT fra SA? (og faktisk behøver
# I ikke eksplicit lave BWT hvis I har SA, for I kan få den
# direkte fra SA).
# our_bwt = bwt.naive(input)

our_bwt = bwt.bwtFromSA(input, SA)
print("BWT\n", our_bwt)

if not ExactSearch:
    # Pas på her! I smidder sentinel i starten af strengen, og det må I ikke.
    # Den skal altid være til sidst.
    rev_bwt = bwt.naive(input[-2::-1].decode() + '$')
    print("BWT of REV INPUT\n", rev_bwt)


c = bwt.c_tabel(input)
print("C TABLE \n", c)


o = bwt.o_table(list(c.keys()), our_bwt)
print("O TABLE\n", o)


if not ExactSearch:
    ro = bwt.o_table(list(c.keys()), rev_bwt)
    # print("RO TABLE\n", ro)


if ExactSearch:
    print("EXACT SEARCH")
    print(f"Searching for {input_search} in {input}")
    i1, i2 = bwt.bwt_search(c, o, input_search)
    for i in range(i1, i2):
        print(i, SA[i], input[SA[i]:])
else:
    print("APPROX SEARCH")
    print(f"Searching for {input_search} in {input}")
    d = app.d_table(input_search, c, ro, SA)
    print("D TABLE\n", d)
    L, R = 0, len(input) # brug et åbent interval.
    i = len(d)-1
    edits = 1
    result = app.recApproxSearch(input_search, i, edits, L, R, d, c, o, list(c.keys()), [])
    for L, R in result:
        for i in range(L, R):
            print(i, SA[i], input[SA[i]:])

    cigars = app.cigar(result, input, input_search, SA, edits)
    print("CIGARS\n", cigars)





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

