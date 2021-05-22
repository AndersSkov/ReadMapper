import numpy as np
import difflib

# We want to implement the BWT approx search also known as the Li-Durbin algorithm since it allows
# one to terminate the search early by creating an additional table called the D table.
# D table has a minimum number of edits, you need to match the rest of the string, and if the number of edits
# is below this, the recursion stops.
# We will be searching from beginning to end in the SA of the reversed string and searching for the reversed pattern

# Det Union pjat kommer ikke til at virke, fordi det er intervaller og ikke indeks
# I samler sammen. Så jeg har givet funktionen en liste som parameter, og så smider
# jeg intervaller i den.
def recApproxSearch(pattern, i, edits, L, R, D, C, O, letters, res):
    # Vi skal tjekke i < 0 før vi tjekker D[i]. Hvis
    # i er negative får vi ikke en fejl i opslaget, men
    # vi får den forkerte værdi.
    if i < 0:
        if R > L and edits >= 0:
            if (L, R) not in res:
                res.append((L, R))
        return res

    if edits < D[i]:
        return res

    # deletion
    recApproxSearch(pattern, i - 1, edits - 1, L, R, D, C, O, letters, res)

    # I denne løkke opdaterer I L og R, men alle I skal jo starte fra det
    # samme interval for hvert tegn!
    oldL, oldR = L, R
    for char in letters[1:]:
        idx = letters.index(char)
        # indeksering og dtype
        L = C[char] + O[oldL, idx]
        R = C[char] + O[oldR, idx]
        if L < R:
            # insert
            recApproxSearch(pattern, i, edits - 1, L, R, D, C, O, letters, res)
            if pattern[i] == char:
                # match
                recApproxSearch(pattern, i - 1, edits, L, R, D, C, O, letters, res)
            else:
                # substitution
                recApproxSearch(pattern, i - 1, edits - 1, L, R, D, C, O, letters, res)

    return res


# A table with an entrance per index in the pattern, and at each index, we will record a lower bound in the number of edits we need.
def d_table(pattern, c, ro, length_of_SA, idx_array):
    table = np.zeros(len(pattern))
    min_edits = 0
    L = 0
    R = length_of_SA
    for i in range(len(pattern)):
        char = pattern[i]
        L = c[char] + ro[L, idx_array[char]]
        R = c[char] + ro[R, idx_array[char]]
        if L >= R:
            min_edits += 1
            L = 0
            R = length_of_SA
        table[i] = min_edits
    return table


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
