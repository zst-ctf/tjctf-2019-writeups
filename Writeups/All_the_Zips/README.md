# All the Zips
Forensics

## Challenge 

140 zips in the zip, all protected by a *dictionary* word.

[all_the_zips.zip](41f4419f4ba027561f22df9fabb56589205c4ec4bf47fa49d5e07cc3910d6d4f_all_the_zips.zip)

## Solution

To [crack the ZIP passwords](https://allanfeid.com/content/cracking-zip-files-fcrackzip), let's use `fcrackzip`.

Initially, I thought of using the [standard `rockyou.txt`](http://downloads.skullsecurity.org/passwords/rockyou.txt.bz2) as the dictionary list. However, it was taking too long

	fcrackzip -v -D -p ./rockyou.txt -u all_the_zips/zip0.zip 

However, the challenge description says it is a dictionary word.

I then thought of using an English dictionary wordlist. https://packages.ubuntu.com/trusty/wordlist

	# apt-get install wamerican
	# ls -la /usr/share/dict                  
	total 960
	drwxr-xr-x 1 root root   4096 Apr  6 03:00 .
	drwxr-xr-x 1 root root   4096 Aug 10  2018 ..
	-rw-r--r-- 1 root root 972398 Apr 24  2018 american-english
	lrwxrwxrwx 1 root root     16 Apr 24  2018 words -> american-english

Doing a test, it seems to be working and cracking in a short amount of time.

	# file='all_the_zips/zip0.zip'
	# fcrackzip -D -u -p /usr/share/dict/words "$file" | grep "PASSWORD FOUND"; done
	PASSWORD FOUND!!!!: pw == how

---

Write a quick bash script to extract all passwords

	for i in {0..139}; do
		file="all_the_zips/zip$i.zip";
		echo "$file";
		fcrackzip -D -u -p /usr/share/dict/words "$file" | grep "PASSWORD FOUND";
	done

	# for i in {0..139}; do file="all_the_zips/zip$i.zip"; echo "$file"; fcrackzip -D -u -p /usr/share/dict/words "$file" | grep "PASSWORD FOUND"; done

Within 5 min or less, all are cracked...

Passwords make a story, but it is not the flag.

	$ cat output1.txt | grep PASSWORD | cut -d '=' -f 3 | tr -d '\n'
	how to establish your dominance at university dominate the room do what i do get one of those fifteen liter water cooler bottles and bring it to class slung over one shoulder slam that mother on the ground in the aisle every time you feel a little thirsty stand up lift the bottle to your mouth with both arms make Lauder you spill plenty of water over yourself and preregistering floor every Christa you do also let out a deep loud sigh of satisfaction after every sip then finish the routine by slamming the bottle on the ground again before loudly saying few i needed that i was getting a bit thirsty yell thirsty as loud as you can when class finishes pick up the bottle in such a way that the remainder pours out as you leave the room

---

I then wrote a Bash script to unzip recursively, and then append each of the zip's flag.txt contents to output2.txt.

	Password_List="how to establish your dominance at university dominate the room do what i do get one of those fifteen liter water cooler bottles and bring it to class slung over one shoulder slam that mother on the ground in the aisle every time you feel a little thirsty stand up lift the bottle to your mouth with both arms make Lauder you spill plenty of water over yourself and preregistering floor every Christa you do also let out a deep loud sigh of satisfaction after every sip then finish the routine by slamming the bottle on the ground again before loudly saying few i needed that i was getting a bit thirsty yell thirsty as loud as you can when class finishes pick up the bottle in such a way that the remainder pours out as you leave the room"
	Passwords=($Password_List)

	echo '' > output2.txt
	for i in {1..139}; do
		pwd=${Passwords[i]};
		unzip -P "$pwd" "all_the_zips/zip$i.zip";
		cat flag.txt >> output2.txt;
		echo '' >> output2.txt;
		rm flag.txt;
	done

And after extracting all flag.txt files, we can find the tjctf flag.

	# cat output2.txt | grep tjctf
	tjctf{sl4m_1_d0wn_s0_that_it5_heard}

## Flag

	tjctf{sl4m_1_d0wn_s0_that_it5_heard}

