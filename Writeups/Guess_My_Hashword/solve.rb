#!/usr/bin/env ruby
require 'digest/md5'

$my_hash = "31f40dc5308fa2a311d2e2ba8955df6c"

def attempt(guess)
	if Digest::MD5.hexdigest("tjctf{#{guess}}") == $my_hash then
		puts "Flag: tjctf{#{guess}}"
		exit
	end
end

# a captial letter, two lowercase letters, a number, and an underscore.
e = '_'
for a in "A".."Z"
	for b in "a".."z"
		for c in "a".."z"
			for d in "0".."9"
				permutes = [a, b, c, d, e].permutation.map &:join
				for guess in permutes
					attempt(guess)
				end
			end
		end
	end
	puts "a=" + a
end
