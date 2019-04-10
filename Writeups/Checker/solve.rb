#!/usr/bin/env ruby

# forward wow()
def forward_wow(s, n)
	a = s.slice(0, n)
	b = s.slice(n, s.length)
	return b + a
end
# reverse wow()
def reverse_wow(x, n)
	a = x.slice(0, x.length-n)
	b = x.slice(x.length-n, x.length)
	return b + a
end

# reverse wow(str, 9)
encoded = "1100001110000111000011000010100001110000111000010100001110000010000110010001011001110000101010001011000001000";
encoded = reverse_wow(encoded, 9)

# reverse woah()
encoded = encoded.gsub!('1', 'x').gsub!('0', '1').gsub('x', '0')

# split up binary bits
# printable chars range from 0x20 to 0x7e
$charset = ('a'..'z').to_a + ('A'..'Z').to_a + ('0'..'9').to_a + ['_', '}', '{']

def retrieve_stack(str, offset, bit_len)
	str.reverse.slice(offset, bit_len).reverse.to_i(2)
end

def solve(encoded, offset, progress)
	# if reached the end successfully, return the progress
	if offset >= encoded.length then
		return progress
	end
	# because the binary bits are not padded to lengths of 8,
	# they can either be 6 bits or 7 bits of ASCII
	for bit_len in 7.downto(6) do
		ascii_byte = retrieve_stack(encoded, offset, bit_len)
		ascii_char = ascii_byte.chr
		if $charset.include?(ascii_char) then
			ret_val = solve(encoded, offset + bit_len, progress + ascii_char)
			if ret_val then
				if ret_val.include? 'tjctf' then
					puts 'Found: ' + ret_val
				end
			end
		end
	end
	return false
end

# use a recursive function to for a "tree" expanding from the front
# it will return when it reaches the end successfully.
# and I did a puts() to print out the possibilities
solve(encoded, 0, '')
