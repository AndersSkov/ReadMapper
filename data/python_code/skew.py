"""
    Skew implementation of suffix array creation
"""
def skew(arg):
    ##########################
    # construct sa0 and sa12 #
    ##########################

    sa0 = sa12 = []
    for i in range(len(arg)):
        if i % 3 == 0:
            sa0.append([i, arg[i:]])
        else:
            sa12.append([i, arg[i:]])
    

    ##########################
    #        sort sa12       #
    ##########################

    # sort sa12 by triplets
    sa12_tri = [[s[0], s[1][:3]] if len(s[1]) >= 3 else [s[0], s[1] + '$' * 3-len([1])] for s in sa12]
    sa12_tri = radix_sort(sa12_tri)

    # assign lex names to sorted triplets
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
            sa12_lex.append([s[0], lex])
            prev = s[1]

    # check if triplets are unique
    if unique:
        # triplets are sorted, convert to sa12
        sa12.clear()
        for s in sa12_tri:
            sa12.append([s[0], arg[:sa[1]]])
    else:
        # create u string and sort recursively
        u_f = ""
        u_l = ""
        for s in sa12_lex[::-1]:
            if s[0] % 3 == 2:
                u_f += str(s[1])
            else:
                u_l += str(s[1])
        u = u_f + "#" + u_l
        u_sorted = skew(u)
    

    ##########################
    #        sort sa0        #
    ##########################

    tmp = []
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