#!/usr/bin/env python3
import socket
import base64
import find_min_distance

if __name__ == '__main__':
    s = socket.socket()
    s.connect(('p1.tjctf.org', 8005))

    collected_data = ''
    while True:
        data = s.recv(40960).decode()
        if not data:
            break

        print("Received:", data)
        collected_data += data

        if '>>> ' in data:
            b64_img = collected_data.split('continue:')[1].split('>>>')[0].strip()
            img = base64.b64decode(b64_img)

            filename = 'solve.png'
            with open(filename, 'wb') as f:
                f.write(img)
            min_dist = find_min_distance.main(filename=filename)

            print('Found distance:', min_dist)
            
            s.send(str(min_dist).encode() + b'\n')
            collected_data = ''

        if 'tjctf{' in data:
            quit()
