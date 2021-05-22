import suffix_array as sa
import numpy as np

def naive(input):
    length = len(input)
    # rotate the input 
    rotations = []
    rotations.append(input)
    for i in range(length-1):
        input = input[1:] + input[0]
        rotations.append(input)

    # sort the rotations lexicografical
    rotations.sort()

    output = ""
    # take the last letter of the sorted rotations
    for i in range(len(rotations)):
        st = rotations[i]
        output = output + st[length-1]

    return output

def naive_inverse(input):
    # create table
    table = []
    for char in input:
        table.append(char)
    table.sort()
    
    for _ in range(1, len(input)):
        for idx in range(len(input)):
            char = input[idx]
            table[idx] = char + table[idx] 
        table.sort()

    # find the word ending with $ 
    output = ""
    for word in table:
        if(word[len(word) - 1] == "$"):
            output = word

    print("Inverse BWT:", output)

    return output

def bwtFromSA(input, SA):
    bwt = ""
    for i in range(len(SA)):
        if SA[i] == 0:
            bwt += "$"
        else:
            inp = input[SA[i]-1]
            bwt += inp
    return bwt


from collections import Counter
def c_tabel(input):
    counts = Counter(input)
    c, accsum, idx_array, i = {}, 0, {}, 0
    for k in sorted(counts):
        c[k] = accsum
        idx_array[k] = i
        accsum += counts[k]
        i += 1
    return c, idx_array


def o_table(chars, bwt):
    num_of_chars = len(chars)
    length_of_bwt = len(bwt)
    o = np.zeros([length_of_bwt + 1, num_of_chars], dtype=int )

    for idx, char in enumerate(chars):
        for i in range(1, length_of_bwt+1):
            o[i, idx] = o[i-1, idx] + (bwt[i-1] == char)

    """""
    for idx, char in enumerate(chars):
        update_value = o[i, idx] + 1
        o[i+1:, idx] = update_value
    """""
    return o


def bwt_search(c, o, search, idx_array):
    L, R = 0, o.shape[0] - 1

    for char in search[::-1]:
        if char not in c:
            return 0, 0
        if L > R:
            break
        L = c[char] + o[L, idx_array[char]]
        R = c[char] + o[R, idx_array[char]]

    return L, R