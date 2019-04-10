# Comprehensive
Reversing

## Challenge 

Please teach me how to be a comprehension master, all my friends are counting on me!

[comprehensive.py](89499ec336d112481a0aa44de40c5aa52b62d3557f1791356fc775877c945545_comprehensive.py)

Original output: 225, 228, 219, 223, 220, 231, 205, 217, 224, 231, 228, 210, 208, 227, 220, 234, 236, 222, 232, 235, 227, 217, 223, 234, 2613

Note: m and k were 24 and 8 characters long originally and english.

## Solution

Program operation

- input is all lowercase
- f, g = cyclic xor(msg, key)
- h = alternating split of array into 8 groups with 3 elements
- i = cyclic xor(array, key[0, 1, 2])
- p = add key[0] to all elements
- print final array[1:-1], meaning print without brackets
- print sum

Solution and explanation all inside my Python3 script:

- [debug.py](debug.py): explains program operation
- [solve.py](solve.py): explains solution techiques

Output

	$ python3 solve.py 
	search_flag_format [116, 106, 99, 116, 102, 123]
	key0_5 b'munchk'
	bruteforce key[0..7]
	do on chunks
	success b'munchkyn' b'tjctf{oooowakarimashita}'

## Flag

	tjctf{oooowakarimashita}
