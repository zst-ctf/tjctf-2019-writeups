# MC Woes
Forensics

## Challenge 

[My world](b9bf0bf0d5572ba9ab95a2e13af6d44b362ed7613fa30bb939d71cb38c5f7833_my_world.zip) won't launch anymore! I'm sure its something in the files...

## Solution

Hint from the Discord group

	its whole "world " full of "data" to explore

With this, I searched all the data files...

	worlddata $ strings level.dat | grep tjctf
	2tjctf{_g3t_sn4ck5}
	
	worlddata $ pwd
	./tjctf-2019/MC_Woes/my world/worlddata


## Flag

	tjctf{_g3t_sn4ck5}
