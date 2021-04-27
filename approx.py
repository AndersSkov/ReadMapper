import bwt
import numpy as np
# We want to implement the BWT approx search also known as the Li-Durbin algorithm since it allows
# one to terminate the search early by creating an additional table called the D table.
# D table has a minimum number of edits, you need to match the rest of the string, and if the number of edits
# is below this, the recursion stops.
# We will be searching from beginning to end in the SA of the reversed string and searching for the reversed pattern

def li_durbin(input, pattern, SA, c_table, ro_table):
    D = d_table(pattern, c_table, ro_table, SA)

    rev_pattern = pattern[::-1]
    rev_SA = SA[::-1]


# A table with an entrance per index in the pattern, and at each index, we will record a lower bound in the number of edits we need.

def d_table(pattern, c_table, ro_table, SA):
    chars = list(c_table.keys())
    table = np.zeros(len(pattern))
    min_edits = 0
    L = 1
    R = len(SA)-1
    for i in range(len(pattern)):
        char = pattern[i]
        idx = chars.index(char)
        L = int(c_table[char] + ro_table[L-1, idx])
        R = int(c_table[char] + ro_table[R, idx]-1)
        if L > R:
            min_edits += 1
            L = 1
            R = len(SA)-1
        table[i] = min_edits
    return table

"""
def search(i, j, k, edits, start, v):

    cigar = []
    i = 0
    j = 0
    k = 0

    if edits < 0:
        return
    if i == v:
        handle_node(j, y, edits)

    if x[i] == y[i]:
        # match
        cigar[k] = 'M'
        search(i+1, j+1, k+1, edits, start, v)
    else:
        # substitute
        cigar[k] = 'M'
        search(i + 1, j + 1, k + 1, edits-1, start, v)

    # try insertion
    cigar[k] = 'I'
    search(i+1, j, k+1, edits-1, start, v)

    # try deletion
    cigar[k] = 'D'
    search(i, j, k + 1, edits - 1, start, v)


def handle_node(j, x, edits):
"""