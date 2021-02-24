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
    

    return 42