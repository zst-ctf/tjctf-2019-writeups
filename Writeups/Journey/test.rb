#!/usr/bin/env ruby
require "socket"

s = TCPSocket.new("p1.tjctf.org", 8009)

data = s.readline
s.puts('king')

flag = ''
while true
    data = s.readline
    puts("Received: " + data)

    if data.include? "tjctf"
        break
    end

    # Encountered 'one'
    m = data.match /Encountered \'(?<word>.+?)\'/
    word = m[:word]

    s.puts(word)
    puts("Send: " + word)

    flag += word + ' '
    puts("Progress: " + flag)
end

s.close
