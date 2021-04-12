"""
    Radix sort method for sorting strings in lists, lexicographically. The sentinel '$' is considered the lowest
    character in this sorting. Assumes input in triplets
"""
def radix_sort(arr):
    # sort by least to most significant idx in arr
    for idx in range(2, -1, -1):
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
        count[ord(s[idx])] += 1
    
    # accumulate count array
    for i in range(len(count)):
        count[i] += count[i-1]
    
    # sort to output array
    for s in arr[::-1]:
        output[count[ord(s[idx])]-1] = s
        count[ord(s[idx])] -= 1
    
    return output
