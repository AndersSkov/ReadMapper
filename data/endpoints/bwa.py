import sys

from data.python_code.approx import d_table, recApproxSearch
from data.python_code.bwt import bwtFromSA, c_tabel, o_table
from data.python_code.suffix_array import SA_IS
from data.python_code.test import read_fasta_file, read_fastq_file


def now():
    if len(sys.argv) != 3:
        print("Please provide a file to parse")
        sys.exit(1)

    fasta_path = sys.argv[1]
    reads_path = sys.argv[2]

    fasta = read_fasta_file(fasta_path)
    fasta_str = fasta[" chr1"]+"$"

    SA = SA_IS(fasta_str, 256)
    BWT = bwtFromSA(fasta_str, SA)
    REV_BWT = bwtFromSA(fasta_str[-2::-1]+"$", SA)
    C, idx_array = c_tabel(fasta_str)
    O = o_table(list(C.keys()), BWT)
    RO = o_table(list(C.keys()), REV_BWT)

    reads = read_fastq_file(reads_path)

    for j in range(len(reads)):
        D = d_table(reads[j], C, RO, SA[0]+1, idx_array)
        L, R = 0, SA[0]+1
        i = len(D)-1
        edits = 1
        result = recApproxSearch(reads[j], i, edits, L, R, D, C, O, list(C.keys()), idx_array, [])
        for L, R in result:
            for k in range(L, R):
                print(k, SA[k], fasta_str[SA[k]: SA[k]+len(reads[j])+edits])


if __name__ == '__main__':
    now()