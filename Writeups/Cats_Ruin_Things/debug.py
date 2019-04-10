#!/usr/bin/env python
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from os import urandom
import struct

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
        
def sign(m, key):
    p = key.p
    q = key.q
    e = key.e
    d = modinv(e, (p-1)*(q-1))
    dp = d%(p-1)
    dq = d%(q-1)+struct.unpack('i', urandom(4))[0]
    qInv = modinv(q, p)
    
    # decrypt using crt
    s1 = pow(m, dp, p)
    s2 = pow(m, dq, q)
    h = (qInv*(s1-s2))%p
    s = s2+h*q
    return [s, e, p*q, p, q]

def decrypt(m, key):
    p = key.p
    q = key.q
    e = key.e
    d = modinv(e, (p-1)*(q-1))
    dp = d%(p-1)
    dq = d%(q-1)
    qInv = modinv(q, p)
    
    # decrypt using crt
    s1 = pow(m, dp, p)
    s2 = pow(m, dq, q)
    h = (qInv*(s1-s2))%p
    s = s2+h*q
    return [s, e, p*q, p, q]
    
    
# f = open("flag.txt", 'r')
flag = "test"

while True:
    press = int(raw_input("Pick an option \n [1] Sign a message [2] Verify your own signature [-1] Adios! \n"))
    key = RSA.generate(2048)
    h = SHA256.new()
    h.update(flag)
    fin = int(h.hexdigest(), 16)
    test = str(key.encrypt(fin, 'x')[0])
    print("flag: " + str(flag))
    print("hexdigest: " + str(h.hexdigest()))
    print("fin: " + hex(fin))
    print("test#: " + hex(int(test)))

    if( press == -1 ):
        print("Hasta luego!")
        break
    elif( press == 1 or press == 2 ):
        mes = raw_input("Enter a message to be signed: ")
        h.update(mes)
        hashm = h.hexdigest()
        mes = int(hashm, 16)
        out = sign(mes, key)
        print("hashm: " + str(hashm))
        print("mes: " + hex(mes))
        print("\nout#: " + hex(int(out[0])))
        dec1 = int((decrypt(int(test), key))[0])
        dec2 = int((decrypt(int(dec1), key))[0])
        print("decrypt(test)  == fin: " + hex(dec1))
        print("decrypt2(test) == out: " + hex(dec2))

        encrypt_out = key.encrypt(int(out[0]), 'x')[0]
        encrypt2_out = key.encrypt(int(encrypt_out), 'x')[0]
        print("encrypt(out)  == fin : " + hex(encrypt_out))
        print("encrypt2(out) == test: " + hex(encrypt2_out))
        
        ############################################################
        # Combining the two partial signatures will give us a faulty final signature.
        # If the signature were correct, we would be able to verify it by comparing the original message
        # s**e (mod n)
        _m = int(test) # correct
        _s = out[0] # faulted
        _e = out[1]
        _n = out[2]
        # since encrypt2(out) == test, we can do the Fault Attack
        _enc_s = pow(_s, _e, _n)
        _enc2_s = pow(_enc_s, _e, _n)

        # Because p is also a factor of n itself, the attacker can take the
        # greatest common denominator of n and s^e-m to extract p.
        from fractions import gcd
        _p = gcd(_n, (_enc2_s - _m) % _n)
        _q = _n // _p
        assert (_p == out[3])
        assert (_q == out[4])

        # decrypt(test)  == fin
        _phi = (_p-1) * (_q-1)
        _d = modinv(_e, _phi)

        _orig = pow(_m, _d, _n)
        print('_orig: ' + str(_orig))
        assert (_enc_s == encrypt_out)
        ############################################################


        print("e: " + str(out[1]))
        print("N: " + str(out[2]))
        if( press == 2 ):
            print("p: " + str(out[3]))
            print("q: " + str(out[4]))
            print("hashed mes: " + str(hashm))
            insig = int(raw_input("What is your signature? "))
            if( int(insig) != out[0] ):
                print("Wrong!")
                continue
            else:
                print("Correct!")
                continue
        else:
            print("Here is your signature:")
            print(str(out[0]) + "\n\n" + "-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-" + "\n")
            #print(fin) #comment out
            check = raw_input("I heard you wanted to steal my treats. You aren't worthy unless you can decrypt " + test + ": ")
            if( int(fin) == int(check) ):
                print(flag)
            else:
                print("Better luck next time!")
            break
    print(" :( ")
    break





