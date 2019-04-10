#!/usr/bin/env ruby
require "chunky_png"

# https://stackoverflow.com/questions/35489257/how-do-i-get-the-hex-value-from-each-pixel-in-rmagick-or-chunky-png
filename = '41862e5c8dd075d112756d754285a5e6218b6f270054a09a23735431b80de9fd_galaxy.png'

# open image
img = ChunkyPNG::Image.from_file(filename)
height = img.dimension.height
width  = img.dimension.width

flag = ''

# retrieve LSB
height.times do |y|
	width.times do |x|
		r = ChunkyPNG::Color.r(img[x,y])
		g = ChunkyPNG::Color.g(img[x,y])
		b = ChunkyPNG::Color.b(img[x,y])

		flag += (r & 0x01).to_s
		flag += (g & 0x01).to_s
		flag += (b & 0x01).to_s
	end
end

# split up binary bits to multiples of 8
binary_string = flag.scan(/.{8}/)

# convert to ascii
ascii_integers = binary_string.map { |string| string.to_i(2) }
ascii_chars = ascii_integers.map { |integers| integers.chr }

puts ascii_chars.join('')
