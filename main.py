import suffix_array as sa
import bwt 

input = "mississippi$"

print("naive implementation of suffix array")
sa.naive(input)

print("skew implementation of suffix array")
sa.skew(input)

print("naive implementation of bwt")
inverse = bwt.naive(input)

print("naive implementation of bwt_inverse")
bwt.naive_inverse(inverse)

