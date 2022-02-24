import numpy as np
import difflib

# We want to implement the BWT approx search also known as the Li-Durbin algorithm since it allows
# one to terminate the search early by creating an additional table called the D table.
# D table has a minimum number of edits, you need to match the rest of the string, and if the number of edits
# is below this, the recursion stops.
# We will be searching from beginning to end in the SA of the reversed string and searching for the reversed pattern
def recApproxSearch(pattern, i, edits, L, R, D, C, O, letters, idx_array, res):
    if i < 0:
        if edits >= 0:
            res.append((L, R))
        return res

    if edits < D[i]:
        return res

    # insertion
    recApproxSearch(pattern, i - 1, edits - 1, L, R, D, C, O, letters, idx_array, res)

    oldL, oldR = L, R
    for char in letters[1:]:
        L = C[char] + O[oldL, idx_array[char]]
        R = C[char] + O[oldR, idx_array[char]]
        if L < R:
            # deletion
            recApproxSearch(pattern, i, edits - 1, L, R, D, C, O, letters, idx_array, res)
            if pattern[i] == char:
                # match
                recApproxSearch(pattern, i - 1, edits, L, R, D, C, O, letters, idx_array, res)
            else:
                # substitution
                recApproxSearch(pattern, i - 1, edits - 1, L, R, D, C, O, letters, idx_array, res)
    return res


# A table with an entrance per index in the pattern, and at each index, we will record a lower bound in the number of edits we need.
def d_table(pattern, c, ro, length_of_SA, idx_array):
    table = np.zeros(len(pattern), dtype=int)
    min_edits = 0
    L = 0
    R = length_of_SA
    for i in range(len(pattern)):
        char = pattern[i]
        L = c[char] + ro[L, idx_array[char]]
        R = c[char] + ro[R, idx_array[char]]
        if R <= L:
            min_edits += 1
            L = 0
            R = length_of_SA
        table[i] = min_edits
    return table


"""
CIGAR string generator doesn't work
"""
def cigar(intervals, input, pattern, SA, edits):
    listOfCIGARS = []
    for L, R in intervals:
        for i in range(L, R):
            temp = ""
            searchIn = input[SA[i]:]
            for j,k in enumerate(difflib.ndiff(searchIn, pattern)):
                if k[0] == ' ':
                    temp += "M"
                elif k[0] == '+':
                    temp += "I"
                elif k[0] == '+':
                    temp += "D"
            listOfCIGARS.append(temp)

    return listOfCIGARS