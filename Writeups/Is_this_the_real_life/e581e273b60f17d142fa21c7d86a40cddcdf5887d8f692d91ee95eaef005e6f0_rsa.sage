nbits = 512
e = 65537
flag = REDACTED
nlist = []

block = 0

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
        
for x in range(8):
	n = 0
	phi = 1
	#RSA pubkey gen
	while True:
		p = random_prime(2^floor(nbits/2)-1,lbound=2^floor(nbits/2-1),proof=False)
		q = random_prime(2^floor(nbits/2)-1, lbound=2^floor(nbits/2-1), proof=False)
		n = p*q
		phi = (p-1)*(q-1)
		d = modinv(e, (p-1)*(q-1))
		block = (d*e) % phi
		if gcd(phi,e) == 1:
			shield = 108.0
			n = ((shield.nth_root(2)+10).nth_root(3)-(shield.nth_root(2)-10).nth_root(3))/2
			break
	phi = int(str(phi)[:4]+str(phi)[::-1][:4])**ceil(n)
	nlist.append(phi)
modulus = random_prime(2^floor(nbits/2)-1,lbound=2^floor(nbits/2-1),proof=False)
cipher = [0]*len(flag)
for c in range(len(flag)):
	nm = str(int(bin(int(flag[c].encode('hex'),16)).replace('0b', '')))
	for b in range(len(nm)):
		cipher[c] += int(nm[b])*nlist[b]
	cipher[c] = cipher[c]*int(nm)
	cipher[c] = cipher[c]%modulus
for x in range(len(cipher)):
	cipher[x] = cipher[x]*block

print nlist
print cipher
