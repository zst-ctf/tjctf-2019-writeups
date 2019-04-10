import string

final_array = [225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234, 2613]
flag_sum = final_array.pop()

# function h
# h = alternating split of array into 8 groups with 3 elements
chunk0 = []
chunk1 = []
chunk2 = []
for i, item in enumerate(final_array):
    if i % 3 == 0:
        chunk0.append(item)
    elif i % 3 == 1:
        chunk1.append(item)
    elif i % 3 == 2:
        chunk2.append(item)

# helper method to check printable chars
# the inputs are lowercase & also english chars & flag format chars
charset = string.ascii_lowercase + string.digits + '}{-_'
printable_chars = bytes(charset, 'ascii')
def all_printable(byte_str):
    return all(char in printable_chars for char in byte_str)

# now, each chunk has 8 elements
# -> chunk 0 is (orig XOR cyclic(key) XOR key[0]) + key[0]
# -> chunk 1 is (orig XOR cyclic(key) by key[1]) + key[0]
# -> chunk 2 is (orig XOR cyclic(key) by key[2]) + key[0]

# since we know the starting flag is `tjctf{`,
# then we can bruteforce key[0] using chunk0
# and reverse key[1..5] using by XOR 'tjctf{'

search_flag_format = [ord(ch) for ch in list('tjctf{')]
print('search_flag_format', search_flag_format)

# realise that the first char of chunk0 is this:
# -> chunk0 is (orig XOR cyclic(key) XOR key[0]) + key[0]
# hence, chunk0[0] = (orig XOR key[0] XOR key[0]) + key[0]
#        chunk0[0] = (orig) + key[0]
#        key[0] = chunk0[0] - (orig)

# do search based on chunk0[0] using 'tjctf{' flag format
# hence, we know the original char is 't'
k0 = chunk0[0] - ord('t')

# now XOR to get key[0..5] using 'tjctf{' flag format
xor_chunk0 = list(map(lambda x: (x - k0) ^ k0, chunk0))
key0_5 = [a ^ b for a, b in zip(xor_chunk0, search_flag_format)]
key0_5 = bytes(key0_5)
print('key0_5', key0_5)

# decrypt helper method
def decrypt_chunk(key, chunkN, N):
    k0 = key[0]
    kN = key[N]
    xor_chunkN = list(map(lambda x: (x - k0) ^ kN, chunkN))
    decrypt_chunkN = [a ^ b for a, b in zip(xor_chunkN, key)]
    return decrypt_chunkN

# for last 2 chars of the key, we can do bruteforce
# the challenge said it is in english, so assume 7-bit ASCII
print('bruteforce key[0..7]')
key_possible = []
for k6 in range(0x7f+1):
    for k7 in range(0x7f+1):
        key = key0_5 + bytes([k6, k7])
        # here, I filtered out non-printable keys
        if all_printable(key):
            key_possible.append(key)

# decrypt each chunk and eliminate non-printables too
print('do on chunks')
for key in key_possible.copy():
    if not all_printable(key):
        key_possible.remove(key)
        continue

    decrypt_chunk0 = decrypt_chunk(key, chunk0, 0)
    if not all_printable(decrypt_chunk0):
        key_possible.remove(key)
        continue

    decrypt_chunk1 = decrypt_chunk(key, chunk1, 1)
    if not all_printable(decrypt_chunk1):
        key_possible.remove(key)
        continue

    decrypt_chunk2 = decrypt_chunk(key, chunk2, 2)
    if not all_printable(decrypt_chunk2):
        key_possible.remove(key)
        continue

# finally, we have the possibilities
# filter out by the flag format ending with }
# and also use sum provided to us to find the correct one
for key in key_possible:
    decrypt_chunk0 = decrypt_chunk(key, chunk0, 0)
    decrypt_chunk1 = decrypt_chunk(key, chunk1, 1)
    decrypt_chunk2 = decrypt_chunk(key, chunk2, 2)
    decrypted = bytes(decrypt_chunk0 + decrypt_chunk1 + decrypt_chunk2)

    if decrypted.endswith(b'}'):
        sum_decrypt = sum([a for a in decrypted])
        if sum_decrypt == flag_sum:
            print('success', key, decrypted)
