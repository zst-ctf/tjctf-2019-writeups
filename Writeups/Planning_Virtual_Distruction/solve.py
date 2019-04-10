#!/usr/bin/env python3
from PIL import Image
import sys


def calculate_bits(P0, P1):
    # After the embedding process, the receiver side will
    # compute the difference of the ith block d′i=|P′i−P′i+1|
    difference = int(abs(P0 - P1))
    # The difference d′i is used to search for the number of
    # concealed bitstreams in the ith block using the quantization range

    # quantization range table
    if 0 <= difference <= 7:
        bits = 3  # R1: pow(2, 3) == 8
        lower = 0
    elif 8 <= difference <= 15:
        bits = 3  # R2: pow(2, 3) == 8
        lower = 8
    elif 16 <= difference <= 31:
        bits = 4  # R3: pow(2, 4) == 16
        lower = 16
    elif 32 <= difference <= 63:
        bits = 5  # R4: pow(2, 5) == 32
        lower = 32
    elif 64 <= difference <= 127:
        bits = 6  # R5: pow(2, 6) == 64
        lower = 64
    elif 128 <= difference <= 255:
        bits = 7  # R5: pow(2, 7) == 128
        lower = 128

    # The secret bitstreams are obtained after converting the
    # decimal value of (d′i−loweri) into binary form.
    secret = difference - lower

    secret_bitstream = bin(secret)[2:].zfill(bits)
    assert (len(secret_bitstream) == bits)

    return secret_bitstream


def split_every_n(line, n):
    return [line[i:i+n] for i in range(0, len(line), n)]


def bin2ascii(inputs):
    return ''.join(map(lambda x: chr(int(x, 2)),
                   split_every_n(inputs, 8)))


filename = 'b4260c304144e942c38edcb1f6d9641c4be1c0f0afee0046b2d50b5342895610_phase2plans.png'
im = Image.open(filename).convert('RGB')
pix = im.load()
width, height = im.size

msg = ''
for h in range(0, height):
    for w in range(1, width, 2):
        # zig zag by going reversed order every odd row
        if (h % 2 == 1):
            w = (-w) % width
        r, g, b = pix[w, h]
        pr, pg, pb = pix[w-1, h]
        msg += calculate_bits(b, pb)

print(bin2ascii(msg))
