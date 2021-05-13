import suffix_array as sa
import bwt 

input = "mississippi$"
input_distinct = "hejmeddig$"
search = "sip"

test = "gatgcgagagatg$"
test_bwt = "ggggggtcaa$taa"
test_search = "gaga"


#print("naive implementation of suffix array")
#suffixes, suf_array = sa.naive(test)
#
print("skew implementation of suffix array")
suf, arr = sa.skew(input)
print(suf)
print(arr)
#
#print("naive implementation of bwt")
#our_bwt = bwt.naive(input)
#
#print("naive implementation of bwt_inverse")
#bwt.naive_inverse(test_bwt)
#
#print("C table")
#c = bwt.c_tabel(test)
#
#print("O table")
#o = bwt.o_table(list(c.keys()), test_bwt)
#
#print("OUR RESULT")
#i1, i2 = bwt.bwt_search(c, o, test_search)
#for i in range(i1, i2+1):
#    print(suffixes[i])
#print(suffixes)
#
#sa.sa_is(input)