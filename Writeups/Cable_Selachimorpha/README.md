# Cable Selachimorpha
Forensics

## Challenge 

Although Omkar is the expert at web, I was still able to intercept his communications. Find out what password he used to login into his website so that we can gain access to it and see what Omkar is up to.

capture.pcap

## Solution

Since it is a website, I filtered by HTTP `tcp.port == 80`

And I see a POST request

	Frame 141: 685 bytes on wire (5480 bits), 685 bytes captured (5480 bits)

	HTML Form URL Encoded: application/x-www-form-urlencoded
	    Form item: "usr" = "omkar"
	    Form item: "pwd" = "tjctf{b0mk4r_br0k3_b10n}"

## Flag

	tjctf{b0mk4r_br0k3_b10n}
