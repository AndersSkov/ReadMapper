from util import radix_sort, counting_sort
import numpy as np
from math import floor, ceil

"""
    Naive implementation of suffix array creation
"""


def naive(input):
    # create all suffixes of input, and sort to array
    suffixes = []

    for i in range(len(input)):
        suffixes.append(input[i:])
    
    suffixes.sort()

    # create suffix array and assign ranks from sorted suffixes
    suffix_array = []

    for suffix in suffixes:
        # get idx of suffix from sorted array
        idx = len(input) - len(suffix)
        suffix_array.append(idx)

    print("suffixes\n", suffixes)
    print("suffix array\n", suffix_array)

    return suffixes, suffix_array


"""
    Skew implementation of suffix array creation
"""


def skew(arg):
    # construct sa0 and sa12 as 2d arrays to keep track of suffix and index
    sa0 = []
    sa12 = []
    for idx in range(len(arg)):
        if idx % 3 == 0:
            sa0.append([idx, arg[idx:]])
        else:
            sa12.append([idx, arg[idx:]])
    print("sa0:", sa0)
    print("sa12:", sa12)
    
    
    # sort sa12
    sa12_tri = [[s[0], s[1][:3]] if len(s[1]) >= 3 else [s[0], s[1] + '$' * (3-len(s[1]))] for s in sa12]
    print("sa12 triplets:", sa12_tri)
    sa12_tri = radix_sort(sa12_tri)
    print("sorted sa12 triplets", sa12_tri)
    # assign lex_name to sorted triplets
    sa12_lex_map = dict()
    sa12_lex = []
    lex = -1
    prev = ""
    done = True
    for s in sa12_tri:
        if s[1] == prev:
            done = False
            sa12_lex.append([s[0], lex])
            continue
        else:
            lex += 1
            sa12_lex_map[lex] = s[1]
            sa12_lex.append([s[0], lex])
            prev = s[1]
    print("sa12_lex", sa12_lex)
    # check if we are done with sa12
    if done:
        tmp = []
        for s in sa12_tri:
            tmp.append([s[0], arg[s[0]:]]) # this is not done, only tri is added
        sa12 = tmp
        print("sa12 with unique tri", sa12)
    else:
        # create u string
        u_f = ""
        u_l = ""
        for s in sa12_lex[::-1]:
            if s[0] % 3 == 2:
                u_f += str(s[1])
            else:
                u_l += str(s[1])
        u = u_f + "#" + u_l
        u_f_arr = [u_f[i:] for i in range(0, len(u_f))]
        u_l_arr = [u_l[i:] for i in range(0, len(u_l))]
        u_arr = u_f_arr + u_l_arr
        # append u_arr with sentinel
        max_len = len((max(u_arr, key = len)))
        u_arr = [s if len(s) == max_len else s + '$' * (max_len-len(s)) for s in u_arr]
        # sort u_arr
        zero_arr = [0 for _ in u_arr]
        u_arr = list(zip(zero_arr, u_arr))
        u_arr = radix_sort(u_arr) # this might need to be recursive
        # extract sorted sa12
        tmp = [""] * len(u_arr)
        for i in range(len(u_arr)):
            for s in u_arr[i][1]:
                if s == "$":
                    continue
                tmp[i] += sa12_lex_map[int(s)]
        # remove redundant '$' in tmp
        for i in range(len(tmp)):
            if tmp[i].find('$') == -1: # no '$' in string
                continue
            tmp[i] = tmp[i][:tmp[i].find('$')+1]
        print(tmp)
        # set sa12 to tmp, with indexes
        sa12 = []
        for s in tmp:
            sa12.append([len(arg) - len(s), s])
    # sort sa0 from sa12
    tmp = []
    for s in sa12:
        if (s[0]) % 3 == 1:
            tmp.append([s[0] - 1, arg[s[0] - 1]  + s[1]])
    sa0 = counting_sort(tmp, 0)
    print(sa0)
    i = j = 0
    sa_idx = [s[0] for s in sa12]
    res = []
    while not (i == len(sa0) and j == len(sa12)):
        if i == (len(sa0)):
            for x in range(j, len(sa12)):
                res.append([ssa12[x][0], sa12[x][1]])
            j = len(sa12)
            continue
        if j == (len(sa12)):
            for x in range(i, len(sa0)):
                res.append([sa0[x][0], sa0[x][1]])
            i = len(sa0)
            continue
        sa0_char = sa0[i][1][0]
        sa12_char = sa12[j][1][0]
        sa0_idx = sa12_idx = -1
        # case 1: j mod 3 = 1
        if sa12[j][0] % 3 == 1:
            sa0_char = sa0[i][1][0]
            sa12_char = sa12[j][1][0]
            if ord(sa0_char) < ord(sa12_char):
                res.append([sa0[i][0], sa0[i][1]])
                i += 1
                continue
            elif ord(sa0_char) > ord(sa12_char):
                res.append([sa12[j][0], sa12[j][1]])
                j += 1
                continue
            sa0_idx = sa_idx.index(sa0[i][0] + 1)
            sa12_idx = sa_idx.index(sa12[j][0] + 1)
        # case 2: j mod 3 = 2
        elif sa12[j][0] % 3 == 2:
            sa0_char = sa0[i][1][0:2]
            sa12_char = sa12[j][1][0:2]
            if (ord(sa0_char[0]) < ord(sa12_char[0])) or (ord(sa0_char[0]) == ord(sa12_char[0]) and ord(sa0_char[1]) < ord(sa12_char[1])):
                res.append([sa0[i][0], sa0[i][1]])
                i += 1
                continue
            elif (ord(sa12_char[0]) < ord(sa0_char[0])) or (ord(sa12_char[0]) == ord(sa0_char[0]) and ord(sa12_char[1]) < ord(sa0_char[1])):
                res.append([sa12[j][0], sa12[j][1]])
                j += 1
                continue
            sa0_idx = sa_idx.index(sa0[i][0] + 2)
            sa12_idx = sa_idx.index(sa12[j][0] + 2)
        print(sa0_idx, sa12_idx)
        if sa0_idx < sa12_idx:
            res.append([sa0[i][0], sa0[i][1]])
            i += 1
            continue
        else:
            res.append([sa12[j][0], sa12[j][1]])
            j += 1
            continue
    print("res", res)
    suf = [s[1] for s in res]
    suf_arr = [s[0] for s in res]
    return suf, suf_arr
                

    

"""
    SA-IS implementation of suffix array creation
"""


def sa_is(input):
    # First up we determine the classes for every char in the input.
    classes = determineClasses(input)
    print("classes:", classes)

    # next up we will find the bucketsize
    bucketSizes = findBucketSizes(input)
    print("bucketsizes:", bucketSizes)
    
    


    return 42


def determineClasses(input):

    L = ord("L")
    S = ord("S")

    # create empty list to fill with L and S
    ret = bytearray(len(input))

    #the last char $ is always S
    ret[-1] = S

    # the second to last char will always be L since everything is larger than $
    ret[-2] = L

    # Step through the rest from right to left
    for i in range(len(input)-2, -1, -1):
        if input[i] > input[i+1]:
            ret[i] = L
        elif input[i] == input[i+1] and ret[i+1] == L:
            ret[i] = L
        else:
            ret[i] = S

    return ret

def findBucketSizes(input, alphabetSize = 256):
    # create a 0 list for the given alphabet size
    # if no size is entered 256 is used as the full range for all characters available from a byte.
    ret = np.zeros(alphabetSize)

    for char in input:
        encode = ord(char)
        ret[encode] += 1

    print(input)
    return ret[ret != 0]