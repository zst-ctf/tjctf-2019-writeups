# Rockstar Certified
Misc

## Challenge 

Tommy is a Certified Rockstar Developer! That means he can code in the [rockstar programming language](https://github.com/RockstarLang/rockstar/blob/master/spec.md).

I've known him for years but last week I saw him dealing with some shady, cultist-y people, exchanging numbers and dates. Just last night, I saw him working on some program called [ritual.rock](b58e1fb8016943a7d3d980340ee707b201985a37d4b96dff5b511ab481658613_ritual.rock). He typed in a number I couldn't see, then the number 1337. The program gave the output 'November 18.' The thing is, November 18th is my favorite day and 1337 is my second favorite number. If the first number he put in is my favorite, I think Tommy here might be a bit of a stalker. And I don't want a cowboy from ram ranch following me around.

Note: the flag is in the format tjctf{[first_number]}

## Solution

### Transpile

I tried the Python transpiler, which did not really work out so well...

	# pip install rockstar-py
	# rockstar-py ritual.rock --output ritual_transpile.py

So nevermind, let's use another one. The ruby one seems to be working better

	sudo apt-get install ruby-full
	gem install kaiser-ruby
	gem install bundler
	gem install pry
	kaiser-ruby transpile ritual.rock > ritual_transpile.rb

Although, the transpiled code doesn't do the function parameters so well so I cleaned it up. I also fixed some of the syntax to make it runnable.

> ritual_cleaned.rb

### Code operation

From the code, here's how it works

- Take 2 inputs from user as (ice, fire)
- ashes = count_one_bits(ice XOR fire)
- ashes / 12 == date
- ashes % 12 == month

Since we have `November 18`, we can get back ashes

	ashes = 12 * date + month
	ashes = 12 * 18 + 11
	ashes = 12 * 18 + 11
	ashes = 227

The 2 inputs are XOR-ed together. Hence, calculate the first input

	first = 227 ^ 1337
	first = 1498

Verify

	$ ruby ritual_cleaned.rb
	> 1498
	> 1337
	November 18

## Flag

	tjctf{1498}
