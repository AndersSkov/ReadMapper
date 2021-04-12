import suffix_array as sa
import numpy as np

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
    

def c_tabel(input):
    temp = dict()
    c = dict()
    # count occurences of chars
    for char in input:
        if not char in temp.keys():
            # create new entrance en dictionary
            temp[char] = 1
        else:
            # increment counter for given char
            value = temp[char]
            temp[char] = value+1
    chars = list(temp.keys())
    temp = sorted(temp.items(), key=lambda kv: kv[0])
    chars.sort()

    # prefix sum
    for i in range(len(temp)):
        if(i == 0):
            c[chars[i]] = 0
        else:
            c[chars[i]] = (c[chars[i-1]] + temp[i-1][1])

    print(c)
    return c

def o_table(chars, bwt):
    num_of_chars = len(chars)
    length_of_bwt = len(bwt)
    o = np.zeros([length_of_bwt, num_of_chars])
    for i in range(length_of_bwt):
        idx = chars.index(bwt[i])
        for j in range(i,length_of_bwt):
            o[j][idx] += 1
    
    print(o)
    return o

def bwt_search(c, o, search):
    chars = list(c.keys())
    print(search)
    L = 1
    R = o.shape[0]-1
    for char in search[::-1]:
        if (L > R):
            break
        idx = chars.index(char)
        L = int(c[char] + o[L-1,idx])
        R = int(c[char] + o[R,idx] - 1)
    
    return L, R