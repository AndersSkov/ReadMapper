from util import radix_sort, counting_sort
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

    return suffixes, suffix_array


"""
    Skew implementation of suffix array creation
"""
def skew(arg):
    ##########################
    # construct sa0 and sa12 #
    ##########################

    sa0 = []
    sa12 = []
    for i in range(len(arg)):
        if i % 3 == 0:
            sa0.append([i, arg[i:]])
        else:
            sa12.append([i, arg[i:]])

    ##########################
    #        sort sa12       #
    ##########################

    # sort sa12 by triplets
    sa12_tri = [[s[0], s[1][:3]] if len(s[1]) >= 3 else [s[0], s[1] + '$' * (3-len(s[1]))] for s in sa12]
    sa12_tri = radix_sort(sa12_tri)
    # assign lex names to sorted triplets
    sa12_lex_map = dict()
    sa12_lex = []
    lex = -1
    prev = ""
    unique = True
    for s in sa12_tri:
        if s[1] == prev:
            unique = False
            sa12_lex.append([s[0], lex])
            continue
        else:
            lex += 1
            sa12_lex_map[lex] = s[1]
            sa12_lex.append([s[0], lex])
            prev = s[1]

    # check if triplets are unique
    if unique:
        # triplets are sorted, convert to sa12
        sa12.clear()
        for s in sa12_tri:
            sa12.append([s[0], arg[s[0]:]])
    else:
        # create u string and sort recursively
        sa12_tri_map = dict()
        for s in sa12_lex:
            sa12_tri_map[s[0]] = s[1]

        u_f = ""
        u_l = ""
        l = len(arg)
        for i in range(l):
            if i % 3 == 0:
                continue
            elif i % 3 == 2:
                u_f += str(sa12_tri_map[i])
            elif i % 3 == 1:
                u_l += str(sa12_tri_map[i])
        u = u_f + "#" + u_l
        u_suf, u_arr = skew(u)

        # extract sorted sa12 from u string
        extract = []
        for s in u_suf:
            tmp = ""
            for c in s:
                if c == "#":
                    break
                tmp += sa12_lex_map[int(c)]
            if tmp == "":
                continue
            extract.append(tmp)
        for i in range(len(extract)):
            if extract[i].find('$') == -1: # no '$' in string
                continue
            extract[i] = extract[i][:extract[i].find('$')+1]
        sa12.clear()
        for s in extract:
            sa12.append([len(arg) - len(s), s])

    ##########################
    #        sort sa0        #
    ##########################

    tmp = []
    if (len(arg) - 1) % 3 == 0:
        tmp.append(sa0[-1])
    for s in sa12:
        if (s[0]) % 3 == 1:
            tmp.append([s[0] - 1, arg[s[0] - 1]  + s[1]])
    sa0 = counting_sort(tmp, 0)

    ##########################
    #   merga sa0 and sa12   #
    ##########################

    i = j = 0
    sa_idx = [s[0] for s in sa12]
    res = []
    while not (i == len(sa0) and j == len(sa12)):
        if i == (len(sa0)):
            for x in range(j, len(sa12)):
                res.append([sa12[x][0], sa12[x][1]])
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
        if sa0_idx < sa12_idx:
            res.append([sa0[i][0], sa0[i][1]])
            i += 1
            continue
        else:
            res.append([sa12[j][0], sa12[j][1]])
            j += 1
            continue
    suf = [s[1] for s in res]
    suf_arr = [s[0] for s in res]
    return suf, suf_arr


"""
    Skew implementation of suffix array creation
"""


def screw(arg):
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


def SA_IS(input):

    # First up we determine the classes for every char in the input.
    classes = determineClasses(input)
    # the classes is stored as a bytearray
    print("CLASSES", classes)
    # next up we will find the bucketsize
    bucketSizes, letters = findBucketSizesAndLetters(input)
    # we don't know where the LMS suffixes should go in our suffix array, so we make a guess
    our_array = LMSsort(input, bucketSizes, classes, letters)

    # when we have our LMS in place we can start to slot all the other suffixes in.
    # we start with L type suffixes
    induceSortL(input, our_array, bucketSizes, classes, letters)
    # next up is S type suffixes
    induceSortS(input, our_array, bucketSizes, classes, letters)

    # create a string that summarises the order of LMS substrings in our_array
    reducedString, reducedAlphabet, reducedOffset = reduceSA(input, our_array, classes)
    print("SUMSTRING", reducedString)

    # making a sorted SA of the reduced string
    reducedSA = sortReducedSA(reducedString, reducedAlphabet)

    # we are here using the SA of the reduced string to determine where the LMS suffixes should be.
    result = accLMSsort(input, bucketSizes, reducedSA, reducedOffset, letters)

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
        if type(char) == int:
            ret[char] += 1
        else:
            ret[ord(char)] += 1
        if(letters.count(char) == 0):
            # we want to know what letters we are working with
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


# We make a suffix array with LMS-substrings approximately by placing them at the end of their bucket
# we guess where the LMS goes with a bucket sort
def LMSsort(input, bucketSize, classes, letters):
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
def induceSortL(input, our_array, bucketSizes, classes, letters):
    heads = bucketHeads(bucketSizes)

    for i in range(len(our_array)):
        # if index = -1, we continue since no suffix is plotted yet here
        if our_array[i] == -1:
            continue

        # we look at the suffix to the left
        left = our_array[i]-1

        if left < 0:
            continue

        if classes[left] != ord("L"):
            # we are only interested in L types
            continue

        # which bucket should we use
        character = input[left]
        index = letters.index(character)
        # we now add the start position at the head of the bucket, and move the tail pointer one up
        our_array[heads[index]] = left
        heads[index] += 1


# we now scan from right to left
# basically a reversed version of the previous function
def induceSortS(input, our_array, bucketSizes, classes, letters):
    tails = bucketTails(bucketSizes)

    for i in range(len(our_array)-1,-1,-1):
        left = our_array[i]-1

        if left < 0:
            continue

        if classes[left] != ord("S"):
            # we only look for S types
            continue

        # which bucket should we use
        character = input[left]
        index = letters.index(character)
        # we now add the start position at the tail of the bucket, and move the tail pointer one down
        our_array[tails[index]-1] = left
        tails[index] -= 1


# we here give each LMS a name based on the order the appear in the our array
# if two LMS suffixes begin with the same LMS substring they get the same name
# These names are combined in the same order as the corresponding suffixes in the original input.
def reduceSA(input, our_array, classes):

    # create a empty list for names
    LMSnames = [-1] * len(input)

    currName = 0

    # we keep track of where the last LMS we checked was in the original input
    lastLMSSuffixOffset = None

    # we know that $ will always be at position 0
    LMSnames[our_array[0]] = currName
    lastLMSSuffixOffset = our_array[0]

    for i in range(1, len(our_array)):
        suffOffset = our_array[i]

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
    # We also build reducedSufOffset, which tells us which LMS suffix each item in the reduced string represents
    reduceSufOffset = []
    reducedString = []

    for index, name in enumerate(LMSnames):
        if name == -1:
            continue

        reduceSufOffset.append(index)
        reducedString.append(name)

    # the smallest is labeled 0 so we add one
    reducedAlphabetSize = currName + 1

    return reducedString, reducedAlphabetSize, reduceSufOffset


def sortReducedSA(reducedString, reducedAlphabetSize):

    if reducedAlphabetSize == len(reducedString):

        # we can make the SA with a bucket sort
        reducedSA = [-1] * (len(reducedString)+1)

        # we include $ at the beginning since its the smallest suffix
        reducedSA[0] = len(reducedString)

        for i in range(len(reducedString)):
            j = reducedString[i]
            reducedSA[j+1] = i

    else:
        # the reduced string is too complex
        # there is at least one letter used more than once, so we can't just bucket sort it, since we don't know where it will go then.
        # recursive
        reducedSA = SA_IS(reducedString, reducedAlphabetSize)
    print("REDUCEDSA", reducedSA)
    return reducedSA


# final SA
# we again place LMS suffixes in with bucket sort, but this time not at random. We use the order determined by the reducedSA
def accLMSsort(input, bucketSizes, reducedSA, reducedOffset, letters):

    sufOff = [-1] * len(input)

    tails = bucketTails(bucketSizes)
    for i in range(len(reducedSA)-1, 0, -1):

        inputIndex = reducedOffset[reducedSA[i]]

        bIndex = input[inputIndex]
        index = letters.index(bIndex)

        sufOff[(tails[index]-1)] = inputIndex
        tails[index] -= 1

    sufOff[0] = (len(input)-1)
    return sufOff
