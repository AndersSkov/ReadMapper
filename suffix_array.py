from util import radix_sort
import numpy as np

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


def skew(str):
    # construct sa0 and sa12 and dict to keep track of index of suffix
    map = dict()
    sa0 = []
    sa12 = []
    for idx in range(len(str)):
        map[str[idx:]] = idx
        if idx % 3 == 0:
            sa0.append(str[idx:])
        else:
            sa12.append(str[idx:])
    print("sa0:", sa0)
    print("sa12:", sa12)
    print("map:", map)
    
    
    # sort sa12
    sa12_tri = [s[:3] if len(s) >= 3 else s + '$' * (3-len(s)) for s in sa12]
    print("sa12 triplets:", sa12_tri)
    sa12_tri = radix_sort(sa12_tri)
    
    # assign lex_name to sorted triplets
    sa12_lex = []
    lex = -1
    prev = ""
    for s in sa12_tri:
        if s == prev:
            sa12_lex.append(lex)
        else:
            lex += 1
            sa12_lex.append(lex)
            prev = s
    print(sa12_lex)

    # check if we are done
    if len(sa12_lex) == len(set(sa12_lex)):
        # we done boys
        pass
    else:
        # create u string
        u_f = ""
        u_l = ""
        for i in range(len(sa12_lex)-1, -1, -1):
            return
        return
        # you done fucked up
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