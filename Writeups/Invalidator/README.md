# Invalidator
Reversing

## Challenge 

Come one, come all! I offer to you unparalleled convenience in getting your flags [invalidated](a70301566b55ac9766935950a79fbd88a58f0bc38aafa3c281dd94c737a9686e_invalidator)!

## Solution

Decompile in Ghidra

	undefined4 main(int param_1,undefined4 *param_2){
	  undefined4 uVar1;
	  int iVar2;
	  undefined4 local_44, local_40, local_3c, local_38, local_34, local_30, local_2c, local_28, local_24, local_20, local_1c, local_18;
	  undefined4 *local_c;
	  
	  local_c = &param_1;
	  if (param_1 < 2) {
	    printf("Usage: %s <flag>\n",*param_2);
	    uVar1 = 1;
	  }else {
	    local_44 = 0x74636a74;
	    local_40 = 0x68307b66;
	    local_3c = 0x5f796d5f;
	    local_38 = 0x31355f34;
	    local_34 = 0x336c706d;
	    local_30 = 0x5f6e3037;
	    local_2c = 0x33725f34;
	    local_28 = 0x33685f64;
	    local_24 = 0x6e317272;
	    local_20 = 0x30665f36;
	    local_1c = 0x68375f72;
	    local_18 = 0x7d3333;
	    iVar2 = strcmp((char *)&local_44,(char *)param_2[1]);
	    if (iVar2 == 0) {
	      puts("Invalid flag.");
	    }
	    else {
	      puts("Valid flag.");
	    }
	    uVar1 = 0;
	  }
	  return uVar1;
	}

At first glance it seems to be comparing to the flag

	irb(main):031:0> [0x74636a74, 0x68307b66, 0x5f796d5f, 0x31355f34, 0x336c706d, 0x5f6e3037, 0x33725f34, 0x33685f64, 0x6e317272, 0x30665f36, 0x68375f72, 0x7d3333].pack("L*")
	=> "tjctf{0h_my_4_51mpl370n_4_r3d_h3rr1n6_f0r_7h33}\x00"

But we realise that it is a red-herring.

If we decompile strcmp(), it is non-standard.

	int strcmp(char *__s1,char *__s2){
	  int local_8;
	  
	  local_8 = 0;
	  while ((*(uint *)(r + (local_8 * 4 + 2) * 4) ==
	          (*(uint *)(r + (local_8 + 0x40) * 0x10) ^
	          (int)__s2[local_8] ^ *(uint *)(r + local_8 * 0x10)) && (__s2[local_8] != 0))) {
	    local_8 = local_8 + 1;
	  }
	  return (uint)(local_8 == 0x28);
	}

Simplify it

	// r is a variable at address 0x0804a040
	// s1 is not used
	int strcmp(char *__s1,char *__s2){
	  int local_8;
	  
	  local_8 = 0;
	  while ((  
	  	r[(local_8 * 4 + 2) * 4] == r[(local_8 + 0x40) * 0x10)] ^ __s2[local_8] ^ r[local_8 * 0x10])
	    && (__s2[local_8] != 0))) {
	    	local_8 = local_8 + 1;
	  }
	  return (uint)(local_8 == 0x28);
	}

The while loop continues until it reaches a null-byte. We can reverse the flag through this

	r[(local_8 * 4 + 2) * 4] == r[(local_8 + 0x40) * 0x10)] ^ __s2[local_8] ^ r[local_8 * 0x10])

	Rearrange...
	__s2[local_8] == r[(local_8 * 4 + 2) * 4] ^ r[(local_8 + 0x40) * 0x10)] ^ r[local_8 * 0x10])

We realise it uses a variable from .data

Let's extract it

	# readelf -x .data invalidator 

Put it into a Ruby script to solve.

	$ ruby solve.rb 
	Flag: tjctf{7h4nk_y0u_51r_0r_m4d4m3_v3ry_c00l}

## Flag

	tjctf{7h4nk_y0u_51r_0r_m4d4m3_v3ry_c00l}
