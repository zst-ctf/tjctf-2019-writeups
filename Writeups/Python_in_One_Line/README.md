# Python in One Line
Reversing

## Challenge 

It's not code golf but it's something...

[one.py](36efc1d21ac49dff41950164dd9c38c77f95a27f3b371ce4293476d601247780_one.py)

 This is printed when you input the flag: 

	.. - / .. ... -. - / -- --- .-. ... / -.-. --- -.. .

## Solution

The code is simply a look_up table

	lookup_dictionary = {'a':'...-', 'b':'--..', 'c':'/', 'd':'-.--', 'e':'.-.', 'f':'...', 'g':'.-..', 'h':'--', 'i':'---', 'j':'-', 'k':'-..-', 'l':'-..', 'm':'..', 'n':'.--', 'o':'-.-.', 'p':'--.-', 'q':'-.-', 'r':'.-', 's':'-...', 't':'..', 'u':'....', 'v':'--.', 'w':'.---', 'y':'..-.', 'x':'..-', 'z':'.--.', '{':'-.', '}':'.'}
	print(' '.join([lookup_dictionary[i] for i in input('What do you want to secrify? ')]))

So we can reverse it

```python
lookup_dictionary = {'a':'...-', 'b':'--..', 'c':'/', 'd':'-.--', 'e':'.-.', 'f':'...', 'g':'.-..', 'h':'--', 'i':'---', 'j':'-', 'k':'-..-', 'l':'-..', 'm':'..', 'n':'.--', 'o':'-.-.', 'p':'--.-', 'q':'-.-', 'r':'.-', 's':'-...', 't':'..', 'u':'....', 'v':'--.', 'w':'.---', 'y':'..-.', 'x':'..-', 'z':'.--.', '{':'-.', '}':'.'}

ct = '.. - / .. ... -. - / -- --- .-. ... / -.-. --- -.. .'
codes = ct.split(' ')

pt = ''
for code0 in codes:
	for (ch, code1) in lookup_dictionary.items():
		if code0 == code1:
			pt += ch

print(pt)
```

We get the text

	mtjcmtf{jchiefcoil}

Remove the `m` for the flag

## Flag

	tjctf{jchiefcoil}
	??