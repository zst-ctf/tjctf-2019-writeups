#!/usr/bin/env ruby
require "nokogiri"
require "open-uri"

$base_link = 'https://moar_horse_2.tjctf.org/'

def retrieve(page)
	link = $base_link + page
	response = open(link) {|f|
		if f.meta.to_s.include? 'tjctf{' then
			raise f.meta.to_s
		end
	}

	response = open(link)
	doc = Nokogiri::HTML(response)
	puts(link + "|" + doc.to_s.strip)

	if doc.to_s.include? 'tjctf{' then
		raise doc.to_s
	end

	a_elements = doc.search('a')
	next_link = a_elements[0]['href']
	prev_link = a_elements[1]['href']
	return [next_link, prev_link]
end

finished = []
pending = []
# threads array
urls = retrieve('4b043a01-a4b7-4141-8a99-fc94fe7e3778.html')
pending += urls

while pending.length > 0
	current = pending.pop
	if finished.include? current then
		next
	end

	finished.push(current)
	urls = retrieve(current)
	pending += urls
	puts pending
	puts ' '
end

'''
urls.each do |url|
  threads << Thread.new(url) do |i|
    resp = open(i)
    puts "#{i} has content length #{resp.read.size} symbols"
  end
end

# run all threads
threads.each { |thr| thr.join }
'''
