# Is this the real life
Crypto

## Challenge 

...is this just fantasy? public key rsagen

## Solution

Looks like RSA

But if we analyse it carefully, it is not quite...

This is my commented code

```python
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
			block = (d*e) % phi ## block == 1
			if gcd(phi,e) == 1:
				shield = 108.0
				n = ((shield.nth_root(2)+10).nth_root(3)-(shield.nth_root(2)-10).nth_root(3))/2
				"""
				sage: shield = 108.0
				sage: ((shield.nth_root(2)+10).nth_root(3)-(shield.nth_root(2)-10).nth_root(3))/2
				1.00000000000000
				"""
				break
		phi = int(str(phi)[:4]+str(phi)[::-1][:4])**ceil(n) 
		## Since n == 1, appends top 4 digits and reversed of bottom 4 digits
		nlist.append(phi)

	# notice that the above RSA keys (n,e,d,phi) are not used.
	# Only the nlist is used from here howards.
	modulus = random_prime(2^floor(nbits/2)-1,lbound=2^floor(nbits/2-1),proof=False)
	cipher = [0]*len(flag)
	for c in range(len(flag)):
		## nm is binary of char. ie 'A' -> '1000001'
		nm = str(int(bin(int(flag[c].encode('hex'),16)).replace('0b', '')))

		# sum all multiplications of nm_bits & nlist[b]
		for b in range(len(nm)):
			cipher[c] += int(nm[b])*nlist[b]

		# multiply by integer representation of the binary string
		cipher[c] = cipher[c]*int(nm)
		# the modulus has no effect because...
		# '11111111' is the maximum possible value to occur
		# but sum(ct) * int('11111111') is still much smaller than modulus
		cipher[c] = cipher[c]%modulus 

	# no effect, block == 1
	for x in range(len(cipher)):
		cipher[x] = cipher[x]*block

	print nlist
	print cipher
```

Hence, we notice that the effective code is as follows

```python
flag = 'REDACTED'
nlist = [42798447, 60070844, 64372735, 50740679, 96064802, 42258424, 44356317, 77336984]

for c in range(len(flag)):
	## nm is binary of char. ie 'A' -> '1000001'
	nm = ord(flag[c]).replace('0b', '')
	# sum all multiplications of nm_bits & nlist[b]
	for b in range(len(nm)):
		cipher[c] += int(nm[b])*nlist[b]
	# multiply by integer representation of the binary string
	cipher[c] = cipher[c]*int(nm)
print nlist
print cipher
```

We can do a quick bruteforce to retrieve the flag.

	$ python3 solve.py 
	tjctf{i_T40ugh7_1t_w43_RsA}

## Flag

	tjctf{i_T40ugh7_1t_w43_RsA}
