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
	
	s1 = pow(m, dp, p)
	s2 = pow(m, dq, q)
	h = (qInv*(s1-s2))%p
	s = s2+h*q
	return [s, e, p*q, p, q]
	
	
f = open("flag.txt", 'r')
flag = f.read()

while True:
	press = int(raw_input("Pick an option \n [1] Sign a message [2] Verify your own signature [-1] Adios! \n"))
	key = RSA.generate(2048)
	h = SHA256.new()
	h.update(flag)
	fin = int(h.hexdigest(), 16)
	test = str(key.encrypt(fin, 'x')[0])
	if( press == -1 ):
		print("Hasta luego!")
		break
	elif( press == 1 or press == 2 ):
		mes = raw_input("Enter a message to be signed: ")
		h.update(mes)
		hashm = h.hexdigest()
		mes = int(hashm, 16)
		out = sign(mes, key)
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





