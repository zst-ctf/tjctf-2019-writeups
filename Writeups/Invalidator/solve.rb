#!/usr/bin/env ruby

# extract data hex dump
data_section = []

f = File.open("data.txt", "r")
f.each_line do |line|
    items = line.split(' ')[1..4]
    hex_str = items.join('').scan(/.{2}/)
    data_section += hex_str.map { |str| str.hex }
end
f.close

# print "data_section: ", data_section, "\n"

# decode according to the formula
# __s2[local_8] == r[(local_8 * 4 + 2) * 4] ^ r[(local_8 + 0x40) * 0x10)] ^ r[local_8 * 0x10])
r = data_section
flag = ''
local_8 = 0
until flag.include? "}"  # until end of flag
    flag_int = r[(local_8 * 4 + 2) * 4].to_i ^ r[(local_8 + 0x40) * 0x10].to_i ^ r[local_8 * 0x10].to_i
    flag += flag_int.chr
    local_8 += 1
end

puts "Flag: " + flag
