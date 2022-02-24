import sys
import cProfile
import tracemalloc

from data.python_code.bwt import bwtFromSA, c_tabel, o_table, bwt_search
from data.python_code.suffix_array import SA_IS
from data.python_code.test import read_fasta_file, read_fastq_file


def now():
    if len(sys.argv) != 3:
        print("Please provide files to parse")
        sys.exit(1)

    fasta_path = sys.argv[1]
    fasta = read_fasta_file(fasta_path)
    fasta_str = fasta[" chr1"] + "$"

    SA = SA_IS(fasta_str, 256)

    BWT = bwtFromSA(fasta_str, SA)
    C, idx_array = c_tabel(fasta_str)
    O = o_table(list(C.keys()), BWT)

    read_path = sys.argv[2]
    reads = read_fastq_file(read_path)

    matches = 0
    for i in range(len(reads)):
        #print(f"Searching for {reads[i]}")
        L, R = bwt_search(C, O, reads[i], idx_array)
        for j in range(L, R):
            matches += 1
            #print(j, SA[j], fasta_str[SA[j]: SA[j]+len(reads[i])])
    print("MATCHES", matches)

if __name__ == '__main__':
    cProfile.run('now()')