from data.python_code import bwt, approx as app, suffix_array as sa

def main():
    input = "mississippi$"
    # baabaabac$
    # gatgcgagagatg$
    # googol$
    input_search = "sip"


    ExactSearch = True


    sa.naive(input)

    SA = sa.SA_IS(input, 256)
    print("SA-IS\n", SA)

    print("skew implementation of suffix array")
    #suf, arr = sa.skew(input)
    #(suf)
    #print(arr)


    our_bwt = bwt.bwtFromSA(input, SA)
    print("BWT\n", our_bwt)

    if not ExactSearch:
        rev_bwt = bwt.naive(input[-2::-1] + '$')
        #print("BWT of REV INPUT\n", rev_bwt)


    c, idx_array = bwt.c_tabel(input)
    #print("C TABLE \n", c)


    o = bwt.o_table(list(c.keys()), our_bwt)
    #print("O TABLE\n", o)


    if not ExactSearch:
        ro = bwt.o_table(list(c.keys()), rev_bwt)
        # print("RO TABLE\n", ro)


    if ExactSearch:
        print("EXACT SEARCH")
        print(f"Searching for {input_search} in {input}")
        i1, i2 = bwt.bwt_search(c, o, input_search, idx_array)
        for i in range(i1, i2):
            print(i, SA[i], input[SA[i]:])
    else:
        print("APPROX SEARCH")
        print(f"Searching for {input_search} in {input}")
        length_of_SA = len(SA)
        d = app.d_table(input_search, c, ro, length_of_SA, idx_array)
        #print("D TABLE\n", d)
        L, R = 0, len(input)
        i = len(d)-1
        edits = 1
        result = app.recApproxSearch(input_search, i, edits, L, R, d, c, o, list(c.keys()), idx_array, [])
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


def read_fastq_file(filename):
    with open(filename) as f:
        content = f.readlines()
        content = [line[:-1] for line in content if not line[0] in '@+~']

    return content

if __name__ == '__main__':
    main()