#!/usr/bin/env ruby
require "socket"

# https://stackoverflow.com/a/45898730
"""
$dictionary_filename = '/usr/share/dict/words/'
def read_file()
	Enumerator.new do |e|
		File.open($dictionary_filename) do |file|
			file.each do |line|
				e << line.strip
			end
		end
	end
end
words = read_file
"""

while true
	s = TCPSocket.new("p1.tjctf.org", 8009)
	while true
		data = s.readline
		puts("Received: " + data)

		if data.include? "tjctf"
			exit
			break
		end

		if data.include? "wrong direction"
			break
		end

		# Encountered 'one'
		m = data.match /Encountered \'(?<word>.+?)\'/
		word = m[:word]
		# word = words.next

		s.puts(word)
		puts("Send: " + word)
	end
	s.close
end
