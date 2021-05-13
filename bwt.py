import suffix_array as sa
import numpy as np

def naive(input):
    length = len(input)
    # rotate the input 
    rotations = []
    rotations.append(input)
    for i in range(length-1):
        input = input[1:] + input[0]
        rotations.append(input)

    # sort the rotations lexicografical
    rotations.sort()

    output = ""
    # take the last letter of the sorted rotations
    for i in range(len(rotations)):
        st = rotations[i]
        output = output + st[length-1]

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

def bwtFromSA(input, SA):
    bwt = ""
    for i in range(len(SA)):
        if SA[i] == 0:
            bwt += "$"
        else:
            inp = input[SA[i]-1]
            bwt += chr(inp)
    return bwt


from collections import Counter
def c_tabel(input):
    counts = Counter(input.decode())
    c, accsum = {}, 0
    for k in sorted(counts):
        c[k] = accsum
        accsum += counts[k]
    return c


def o_table(chars, bwt):
    num_of_chars = len(chars)
    length_of_bwt = len(bwt)
    # Setter dtype her, istedet for at caste ved alle opslag
    # Jeg har lavet tabellen en række længere for at gøre
    # indekseringen nemmere. Det spilder lidt plads, men hvis det
    # er et problem skal vi alligevel bruge en anden kodning af
    # tabellen (wavelettræ og Jacobson's Rank).
    o = np.zeros([length_of_bwt + 1, num_of_chars], dtype=int)
    # Det her kører i kvadratisk tid. Det skal I have ned i lineær tid!
    # I kan opdaterer hver indgang ved at kikke på den foregående, i stedet
    # for at løbe hele resten af tabellen igennem.
    for i in range(length_of_bwt):
        idx = chars.index(bwt[i])
        update_value = o[i, idx] + 1
        o[i+1:, idx] = update_value

    return o


def bwt_search(c, o, search):
    chars = list(c.keys())
    # Håndteringen af L og R bliver meget nemmere hvis man bruger
    # den version fra min bog, så det har jeg skrevet det om til at gøre
    L, R = 0, o.shape[0] - 1
    for char in search[::-1]:
        # tjek c og ikke chars; konstant tid vs linear
        if char not in c:
            # Denne her hopper jo bare over ukendte tegn.
            # Det er jo et mismatch, så I burde stoppe søgningen.
            #continue
            return 0, 0
        if L > R:
            break
        idx = chars.index(char) # linear søgning. Remap først eller noget.
        # Jeg satte dtype for o-tabellen så det ikke er nødvendigt at bruge
        # int() hver gang I slår op i den. Med den anden indeksering slipper vi
        # for nogle off-by-one fejl, og håndteringen bliver symmetrisk.
        L = c[char] + o[L, idx]
        R = c[char] + o[R, idx]

    return L, R # Nu returnerer vi et åbent interval