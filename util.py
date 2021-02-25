"""
    Radix sort method for sorting strings in lists, lexicographically. The sentinel '$' is considered the lowest
    character in this sorting.
"""
def radix_sort(input):
    # find maximum number of characters in input array
    max = -1
    for str in input:
        if len(str) > max:
            max = len(str)

    # prepend all string in input array shorter than max with '$'
    for i in range(len(input)):
        input[i] = input[i] + '$' * (max - len(input[i]))

    iter = max
    temp = input
    while iter >= 0:
        temp = counting_sort(temp, iter)
        iter -= 1

    return temp


"""
    Counting sort subroutine used in radix sort.
"""

def counting_sort(input, idx):
    length = len(input)

    # initialize output and count array
    output = [""] * length
    count = [0] * 256  # output length of 256, to cover all ASCII letters

    # populate count array
    for thingamajig in input:
        order = ord(thingamajig[idx])
        output[order] += 1

    # build the output array
    i = length - 1
    while i >= 0:
        order = ord(input[i][idx])
        output[count[order]] = input[i]
        count[order] -= 1
        i -= 1

    return output
