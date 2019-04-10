import itertools
m = 'tjctf{?????????????????}'.lower()
k = '????????'.lower()

print('msg', list(map(ord, m)))
print('key', list(map(ord, k)))

#########################################
# f = cycle through the key, k and XOR it with msg, m.
f = [[ord(k[a]) ^ ord(m[a+b]) for a in range(len(k))] for b in range(0, len(m), len(k))]
print('f', f)

# g = flatten array
g = [a for b in f for a in b]
print('g', g)

# effectively, f and g do a cyclic-XOR.
# ie. XOR(m, cycle(k))
cyclic_xor = [ord(a) ^ ord(b) for a, b in zip(m, itertools.cycle(k))]
print('cyclic_xor', cyclic_xor)
assert cyclic_xor == g

#########################################
# Testing
#f[0] = ['1'] * 4
#import string
#g = string.ascii_letters
#h = [[g[a] for a in range(b, len(g), len(f[0]))] for b in range(len(f[0]))]

#########################################
# h = split up g into multiple arrays where each item is alternated into each array
# eg. g = abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
# eg. h= [['a', 'e', 'i', 'm', 'q', 'u', 'y', 'C', 'G', 'K', 'O', 'S', 'W'], ['b', 'f', 'j', 'n', 'r', 'v', 'z', 'D', 'H', 'L', 'P', 'T', 'X'], ['c', 'g', 'k', 'o', 's', 'w', 'A', 'E', 'I', 'M', 'Q', 'U', 'Y'], ['d', 'h', 'l', 'p', 't', 'x', 'B', 'F', 'J', 'N', 'R', 'V', 'Z']]
h = [[g[a] for a in range(b, len(g), len(f[0]))] for b in range(len(f[0]))]
print('g', g)
print('h', h)

# i = xor each group with first 3 chars of the key
i = [[h[b][a] ^ ord(k[a]) for a in range(len(h[0]))] for b in range(len(h))]
print('i', i)

#########################################
# len(f[0]) should be the length of the key
assert len(k) == len(f[0])
# len(h[0]) should be the number of groups, ie. len(m) / len(k)
assert (len(m) // len(k)) == len(h[0])
# len(h[0]) should be the length of the key
assert len(h) == len(k)


#########################################
#print(str([a + ord(k[0]) for b in i for a in b])[1:-1] + ',', sum([ord(a) for a in m]))

sum_flag = sum([ord(a) for a in m])

# final_array = flatten array, then add the first char of the key
final_array = str([a + ord(k[0]) for b in i for a in b])
print('final_array', final_array)

# print without brackets
print(final_array[1:-1] + ',', sum_flag)

test = '225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234, 2613'
if test == (final_array[1:-1] + ',', sum_flag):
	print('Match')
