
def naive(input):
    length = len(input)

    # rotate the input 
    rotations = []
    rotations.append(input)
    for i in range(length-1):
        input = input[1:]+input[0]
        rotations.append(input)

    # sort the rotations lexicografical
    rotations.sort()

    output = ""
    # take the last letter of the sorted rotations
    for i in range(len(rotations)):
        st = rotations[i]
        output = output + st[length-1]
    
    print("BWT:", output)
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