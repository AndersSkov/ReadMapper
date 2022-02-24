import cProfile
import sys
import numpy as np
from datetime import datetime

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
    length_of_SA = SA[0]+1

    reads = read_fastq_file(reads_path)
    matches = 0
    #now = datetime.now().time()
    #print("Start time", now)
    D1 = np.zeros(len(reads[0]))
    for j in range(len(reads)):
        #D2 = d_table(reads[j], C, RO, length_of_SA, idx_array)
        L, R = 0, length_of_SA
        i = len(D1)-1
        edits = 0
        result = recApproxSearch(reads[j], i, edits, L, R, D1, C, O, list(C.keys()), idx_array, [])
        for L, R in result:
            for k in range(L, R):
                matches += 1
                #print(k, SA[k], fasta_str[SA[k]: SA[k]+len(reads[j])+edits])
        #now = datetime.now().time()
        #print(f"time at iteration {j}:", now)
    print("MATCHES", matches)

if __name__ == '__main__':
    cProfile.run('now()')