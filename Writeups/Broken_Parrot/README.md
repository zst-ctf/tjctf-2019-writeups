# Broken Parrot
Reversing

## Challenge 

I found this annoying parrot. I wish I could just ignore it, but I've heard that it knows something special.

## Solution

Decompiled in Ghidra

	v1 = "tjctf{my_b3l0v3d_5qu4wk3r_w0n7_y0u_l34v3_m3_4l0n3}";

	void main(undefined4 param_1,undefined4 param_2){
	  bool bVar1;
	  char local_47 [6];
	  char acStack65 [4];
	  char acStack61 [41];
	  do {
	    while( true ) {
	      printf("Say something to the parrot: ");
	      fgets(local_47,0x33,stdin);
	      if (strlen(local_47); == 0x22) break;
	      printf("%s",local_47);
	    }
	    bVar1 = true;
	    
	    int local_54 = 0;
	    while (local_54 < 6) {
	      if (local_47[local_54] != v1[local_54]) {
	        bVar1 = false;
	      }
	      local_54 = local_54 + 1;
	    }
	    
	    int local_50 = 0;
	    while (local_50 < 3) {
	      if (acStack65[local_50] != v1[local_50 + 0xe]) {
	        bVar1 = false;
	      }
	      local_50 = local_50 + 1;
	    }
	    
	    int local_4c = 0;
	    while (local_4c < 0x17) {
	      if (acStack61[local_4c] != v1[local_4c + 0x1b]) {
	        bVar1 = false;
	      }
	      local_4c = local_4c + 1;
	    }
	    if (acStack65[3] != 'd') {
	      bVar1 = false;
	    }
	    if (bVar1) {
	      puts("You got my flag!");
	    }
	    else {
	      printf("a %s",local_47);
	    }
	  } while( true );
	}

The code checks for certain portions of the hardcoded flag

Parse in Python

	>>> v1 = "tjctf{my_b3l0v3d_5qu4wk3r_w0n7_y0u_l34v3_m3_4l0n3}"
	>>> v1[0:6] + v1[0xe:0xe+3] + 'd' + v1[0x1b:0x1b+0x17]
	'tjctf{3d_d0n7_y0u_l34v3_m3_4l0n3}'

## Flag

	tjctf{3d_d0n7_y0u_l34v3_m3_4l0n3}

