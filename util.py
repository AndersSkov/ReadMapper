"""
    Radix sort method for sorting strings in lists, lexicographically. The sentinel '$' is considered the lowest
    character in this sorting. Assumes input in triplets

    arr is a 2d array, with first entrance containing index, and second entrance containing triplet
"""
def radix_sort(arr, l = -1):
    # sort by least to most significant idx in arr
    length = l
    if l == -1:
        length = len(arr[0])-1
    for idx in range(length, -1, -1):
        arr = counting_sort(arr, idx)
    return arr


"""
    Counting sort subroutine used in radix sort.
"""

def counting_sort(arr, idx):
    # output array
    output = [""] * len(arr)

    # count array
    count = [0] * 256
    
    # populate count array
    for s in arr:
        count[ord(s[1][idx])] += 1
    
    # accumulate count array
    for i in range(len(count)):
        count[i] += count[i-1]
    
    # sort to output array
    for s in arr[::-1]:
        output[count[ord(s[1][idx])]-1] = s
        count[ord(s[1][idx])] -= 1
    
    return output
