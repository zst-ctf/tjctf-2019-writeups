#!/usr/bin/env python3
import socket
from math import gcd


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def get_original_message(n, e, out0, test):
    """
    encrypt(out) == fin == hashm
    encrypt2(out) == test
    fin == decrypt(fin)
    out == decrypt2(test)
    """
    ############################################################
    # Combining the two partial signatures will give us a faulty final signature.
    # If the signature were correct, we would be able to verify it by comparing the original message
    # s**e (mod n)
    _m = test  # correct
    _s = out0  # faulted
    _e = e
    _n = n
    # since encrypt2(out) == test, we can do the Fault Attack
    _enc_s = pow(_s, _e, _n)
    _enc2_s = pow(_enc_s, _e, _n)

    # Because p is also a factor of n itself, the attacker can take the
    # greatest common denominator of n and s^e-m to extract p.

    _p = gcd(_n, (_enc2_s - _m) % _n)
    _q = _n // _p

    # decrypt(test) == fin
    _phi = (_p-1) * (_q-1)
    _d = modinv(_e, _phi)

    _orig = pow(_m, _d, _n)
    return _orig


if __name__ == '__main__':
    s = socket.socket()
    s.connect(('p1.tjctf.org', 8006))

    while True:
        data = s.recv(4096).decode()
        if not data:
            break

        print("Received:", data)

        if 'Pick an option' in data:
            s.send(b'1\n')

        if 'Enter a message to be signed:' in data:
            s.send(b'\n')
            break

    collected_data = ''
    while True:
        data = s.recv(4096).decode()
        if not data:
            break
        print("Received:", data)
        collected_data += data

        # ready for user input
        if collected_data.strip().endswith(':'):
            n = int(collected_data.split('N: ', 1)[1].split('\n', 1)[0].strip())
            e = int(collected_data.split('e: ')[1].split('\n')[0].strip())
            out0 = int(collected_data.split('signature:\n')[1].split('\n')[0].strip())
            test = int(collected_data.split('unless you can decrypt ')[1].split('\n')[0].replace(':', '').strip())
            '''
            print("n", n)
            print("e", e)
            print("out0", out0)
            print("test", test)
            '''
            orig = get_original_message(n, e, out0, test)
            s.send(str(orig).encode() + b'\n')
