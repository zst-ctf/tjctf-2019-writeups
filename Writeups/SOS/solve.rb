require "wavefile"
include WaveFile

########################################################
## retrieve high and low bits
bool_buffer = []
threshold = 500

Reader.new("morse.wav").each_buffer do |buffer|
	for s in buffer.samples
		is_high = (s.abs > threshold) ? 1 : 0
		bool_buffer.push(is_high)
	end
end
# puts bool_buffer.join('')

########################################################
## convert to (amplitude, length)

# split based on same chars, https://stackoverflow.com/a/39030231
split_bool_buffer = bool_buffer.join('').scan(/0+|1+/)
# then count sample length
signal_buffer = split_bool_buffer.map { |st| [st[0], st.length] }
# puts signal_buffer.join(',')

########################################################
# Clean up these observations:
# 35 LOW = part of dit-dah (can be ignored)
# 300 HIGH = part of dit-dah (can be merged)
# 11000 LOW = gap between dits, dahs
# 33000 LOW = gap betwee characters

# Splitting:
# a. Split up characters based on 33000 LOW
# b. Split up dits & dahs based on 11000 LOW
# c. Determine length (dit or dah) based on size of dit-dah count.

morse_code_array = []

morse_code = ''
ditdah_count = 0
ditdah_count_2 = 0
ditdah_threshold = 45 

for sig in signal_buffer
	bit_type = sig[0]
	bit_length = sig[1]
	# puts(bit_type.to_s + '/' + bit_length.to_s)

	# Step1: Count number of 300 HIGH until we reach a 11000 LOW
	if bit_length.between?(300, 400) and bit_type == '1' then
		ditdah_count += 1
	end
	if bit_length.between?(30, 40) and bit_type == '0' then
		ditdah_count_2 += 1
	end
	
	# Step2: when reaching any gap, determine ditdah length and reset
	gap_between_ditdah = (bit_length.between?(10800, 11200) and bit_type == '0')
	gap_between_chars = (bit_length.between?(33000, 33300) and bit_type == '0')

	if gap_between_ditdah or gap_between_chars then
		if ditdah_count < 2 then
			morse_code += ''
		elsif ditdah_count > ditdah_threshold then
			morse_code += '-'
		else
			morse_code += '.'
		end
		puts(ditdah_count.to_s + ' / ' + ditdah_count_2.to_s + ' / ' + morse_code)
		ditdah_count = 0
		ditdah_count_2 = 0
	end
	
	# Step2: end of the character and decode it
	if gap_between_chars then
		morse_code_array.push(morse_code)
		morse_code = ''
	end
end
# puts morse_code_array

########################################################
# Decode:
$morse_dict = {
    "a" => ".-","b" => "-...","c" => "-.-.","d" => "-..","e" => ".","f" => "..-.","g" => "--.","h" => "....","i" => "..","j" => ".---","k" => "-.-","l" => ".-..","m" => "--","n" => "-.","o" => "---","p" => ".--.","q" => "--.-","r" => ".-.","s" => "...","t" => "-","u" => "..-","v" => "...-","w" => ".--","x" => "-..-","y" => "-.--","z" => "--.."," " => " ","1" => ".----","2" => "..---","3" => "...--","4" => "....-","5" => ".....","6" => "-....","7" => "--...","8" => "---..","9" => "----.","0" => "-----"
}
def decode_morse(morse_code)
	# return $morse_dict.select{|key, val| val == morse_code }.keys
	return $morse_dict.key(morse_code) || '?'
end


decoded_array = morse_code_array.map { |code| decode_morse(code) }

puts morse_code_array.join(' ')
puts decoded_array.join('')
