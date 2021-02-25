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

    return suffix_array

"""
    Skew implementation of suffix array creation
"""
def skew(input):
    # create suffixes of input for idx % 3 != 0
    suffixes_12 = []

    for i in range(len(input)):
        if i % 3 == 0:
            continue
        suffixes_12.append(input[i:])
    
    print(suffixes_12)
    
    # sort by prefix triplet in linear time, using radix sort
    
    
        

"""
    SA-IS algorithm
"""


def SA_IS(input):

    # First up we determine the classes for every char in the input.
    classes = determineClasses(input)
    # print(classes)

    # next up we will find the bucketsize
    bucketSizes = findBucketSizes(input)
    print(bucketSizes)

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