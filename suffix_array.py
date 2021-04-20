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





def SA_IS(input, alphabetSize):

    # First up we determine the classes for every char in the input.
    classes = determineClasses(input)
    # the classes is stored as a bytearray

    # next up we will find the bucketsize
    bucketSizes, letters = findBucketSizesAndLetters(input)

    # we don't know where the LMS suffixes should go in our suffix array, so we make a guess
    guessedSA = guessLMSsort(input, bucketSizes, classes, letters)

    # when we have our LMS in place we can start to slot all the other suffixes in.
    # we start with L type suffixes
    induceSortL(input, guessedSA, bucketSizes, classes, letters)
    # next up is S type suffixes which is not LMS.
    induceSortS(input, guessedSA, bucketSizes, classes, letters)

    # create a string that summarises the order of LMS in the guessedSA
    sumString, sumAlphabet, sumOffset = summariseSA(input, guessedSA, classes)

    # making a sorted SA of the summary string
    summarySA = sumSA(sumString, sumAlphabet)

    # we are here using the SA of the summary string to determine where the LMS suffixes should be.
    result = accLMSsort(input, bucketSizes, summarySA, sumOffset, letters)

    # we again slot all the other suffixes in
    induceSortL(input, result, bucketSizes, classes, letters)
    induceSortS(input, result, bucketSizes, classes, letters)

    return result


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


def isLeftMostSmallChar(offset, classes):
    if offset == 0:
        return False
    if classes[offset] == ord("S") and classes[offset-1] == ord("L"):
        return True
    return False


def isLMSsubstringEqual(input, classes, offsetA, offsetB):

    if offsetA == len(input) or offsetB == len(input):
        # no other substring is equal to $
        return False

    i = 0
    while True:
        aLMS = isLeftMostSmallChar(i+offsetA, classes)
        bLMS = isLeftMostSmallChar(i+offsetB, classes)

        # true if we have found the start of the next LMS substring
        if(i>0 and aLMS and bLMS):
            # we have gone through the original LMS substrings without finding differences
            return True

        if aLMS != bLMS:
            # One substring is longer than the other
            return False

        if input[i+offsetA] != input[i+offsetB]:
            # different characters
            return False

        i += 1


def findBucketSizesAndLetters(input, alphabetSize = 256):
    # create a 0 list for the given alphabet size
    # if no size is entered 256 is used as the full range for all characters available from a byte.
    ret = np.zeros(alphabetSize)
    letters = []
    for char in input:
        ret[char] += 1
        if(letters.count(char) == 0):
            letters.append(char)

    letters.sort()
    return ret[ret != 0], letters


def bucketHeads(bucketSizes):
    offset = 0
    ret = []
    for size in bucketSizes:
        ret.append(offset)
        offset += int(size)
    return ret


def bucketTails(bucketSizes):
    offset = 0
    ret = []
    for size in bucketSizes:
        offset += int(size)
        ret.append(offset)
    return ret


# We make a suffix array with LMS-substrings approximately by guessing
# we guess where the LMS goes with a bucket sort
def guessLMSsort(input, bucketSize, classes, letters):
    # empty SA
    SA = [-1] * (len(input))

    tails = bucketTails(bucketSize)
    # bucket sort the LMS approx into the buckets
    for i in range (len(input)):

        # if not LMS, continue
        if not isLeftMostSmallChar(i, classes):
            continue
        # find the index of the character in buckets
        character = input[i]
        index = letters.index(character)
        # we now add the start position at the tail of the bucket, and move the tail pointer one down
        SA[tails[index]] = i
        tails[index] -= 1

    SA.append(SA.pop(0))

    return SA


# for each suffix in our guessed SA we check the suffix to the left in the original input, if it's L-type we bucket sort.
# we scan from left to right
def induceSortL(input, guessedSA, bucketSizes, classes, letters):
    heads = bucketHeads(bucketSizes)

    for i in range(len(guessedSA)):
        # if index = -1, we continue since no suffix is plotted yet here
        if guessedSA[i] == -1:
            continue

        # we look at the suffix to the left
        left = guessedSA[i]-1

        if left < 0:
            continue

        if classes[left] != ord("L"):
            # we are only interested in L types
            continue

        # which bucket should we use
        character = input[left]
        index = letters.index(character)
        # we now add the start position at the head of the bucket, and move the tail pointer one up
        guessedSA[heads[index]] = left
        heads[index] += 1


# we now scan from right to left
# basically a reversed version of the previous function
def induceSortS(input, guessedSA, bucketSizes, classes, letters):
    tails = bucketTails(bucketSizes)

    for i in range(len(guessedSA)-1,-1,-1):
        left = guessedSA[i]-1

        if left < 0:
            continue

        if classes[left] != ord("S"):
            # we only look for S types
            continue

        # which bucket should we use
        character = input[left]
        index = letters.index(character)
        # we now add the start position at the tail of the bucket, and move the tail pointer one down
        guessedSA[tails[index]-1] = left
        tails[index] -= 1


# we here give each LMS a name based on the order the appear in the guessedSA
# if two LMS suffixes begin with the same LMS substring they get the same name
# These names are combined in the same order as the corresponding suffixes in the original input.
def summariseSA(input, guessedSA, classes):

    # create a empty list for names
    LMSnames = [-1] * len(input)

    currName = 0

    # we keep track of where the last LMS we checked was in the original input
    lastLMSSuffixOffset = None

    # we know that $ will always be at position 0
    LMSnames[guessedSA[0]] = currName
    lastLMSSuffixOffset = guessedSA[0]

    for i in range(1, len(guessedSA)):
        suffOffset = guessedSA[i]

        if not isLeftMostSmallChar(suffOffset, classes):
            # is not an LMS suffix
            continue

        # if this LMS suffix is different from the prev we looked at it gets a new name
        if not isLMSsubstringEqual(input, classes, lastLMSSuffixOffset, suffOffset):
            currName += 1

        # update the last LMS suffix
        lastLMSSuffixOffset = suffOffset

        # store the name in the empty list in the same place as it occurs in the original input
        LMSnames[suffOffset] = currName

    # LMSnames now contains all chars of the suffix string in correct order but also a lot of unused indecis we want to remove
    # We also build sumSufOffset, which tells us which LMS suffix each item in the summary string represents
    sumSufOffset = []
    sumString = []

    for index, name in enumerate(LMSnames):
        if name == -1:
            continue

        sumSufOffset.append(index)
        sumString.append(name)

    # the smallest is labeled 0 so we add one
    sumAlphabetSize = currName + 1

    return sumString, sumAlphabetSize, sumSufOffset


def sumSA(sumString, sumAlphabetSize):

    if sumAlphabetSize == len(sumString):

        # we can make the SA with a bucket sort
        summarySA = [-1] * (len(sumString)+1)

        # we include $ at the beginning
        summarySA[0] = len(sumString)

        for i in range(len(sumString)):

            j = sumString[i]
            summarySA[j+1] = i

    else:
        # recursive
        print("REKRUSION")
        summarySA = SA_IS(sumString, sumAlphabetSize)

    return summarySA


# final SA
# we again place LMS suffixes in with bucket sort, but this time not at random. We use the order determined by the summarySA
def accLMSsort(input, bucketSizes, summarySA, sumOffset, letters):

    sufOff = [-1] * len(input)

    tails = bucketTails(bucketSizes)

    for i in range(len(summarySA)-1, 0, -1):

        inputIndex = sumOffset[summarySA[i]]

        bIndex = input[inputIndex]
        index = letters.index(bIndex)

        sufOff[(tails[index]-1)] = inputIndex
        tails[index] -= 1

    sufOff[0] = (len(input)-1)
    return sufOff

