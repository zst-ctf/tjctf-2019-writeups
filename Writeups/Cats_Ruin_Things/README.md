# Cats Ruin Things
Crypto

## Challenge 

My cat took over my computer and ruined everything. Or maybe, only half of everything? [source](107853e7123432ac8e83abd6a39d326bbdbd1955dd3814fc9a27e33ee95184b2_rsa.py)

nc p1.tjctf.org 8006



## Solution

#### Program operation

We are given an RSA program which signs a flag. This is the signing process

	def sign(m, key):
	    p = key.p
	    q = key.q
	    e = key.e
	    d = modinv(e, (p-1)*(q-1))
	    dp = d%(p-1)
	    dq = d%(q-1)+struct.unpack('i', urandom(4))[0]
	    qInv = modinv(q, p)
	    
	    # decrypt using crt
	    s1 = pow(m, dp, p)
	    s2 = pow(m, dq, q)
	    h = (qInv*(s1-s2))%p
	    s = s2+h*q
	    return [s, e, p*q, p, q]

Here, `m` is decrypted using RSA Chinese Remainder Theorem (CRT), but slightly modified. We notice that `dq` has been modified to include some error.

To compare, here's a [standard RSA CRT decryption](https://github.com/lanjelot/ctfs/blob/master/scripts/crypto/rsa/decrypt-rsa-crt.py) program.


#### Fault Analysis Attack (RSA CRT)

This is a some very good articles on the Fault Analysis Attack.

- https://blog.trailofbits.com/2018/08/14/fault-analysis-on-rsa-signing/
- https://www.cryptologie.net/article/371/fault-attacks-on-rsas-signatures/

In short, without errors, this will hold true, where `p` and `q` are factors.

	m = s^e mod p
	m = s^e mod q
	m = s^e mod n

But since `q` has a fault, `p` can be recovered, since `q` is no longer a factor.

	p = gcd( n, (s^e - m) % n )

Now, in context of the program, we have the following information

	> Given: flag
	  fin = hash(flag)
	  test = pow(fin, e) % n

	> Given: mes
	  hashm = hash(flag+mes)
	  out = rsa_decrypt_crt(hashm, random_error)

	> Outputs: test
	> Outputs: out

So with this, if we assume the random error to be zero, these equations will be true.

	# if random_error == 0,
	# Encryption: out -> hashm/fin -> test
	
	fin == hashm
	encrypt(out) == fin
	encrypt2(out) == test
	fin == decrypt(fin)
	out == decrypt2(test)

	# given test, out

So with this, we can apply only encryption. We shall use these equations to do the fault analysis attack. We will compare `test_original` and `test_faulted`.

	test_original
	encrypt(out) == fin_faulted
	encrypt2(out) == test_faulted

Put it all into a script

	$ python3 solve.py 
	Received: Pick an option 
	 [1] Sign a message [2] Verify your own signature [-1] Adios! 

	Received: Enter a message to be signed: 
	Received: e: 65537
	Received: 
	N: 28662740426094805307088621857974031143610833843646591346882618386337332835343672331844778981348967653931316129344751337827333571287927616565964871063974527404220259124378197710410251412594386067954743269227370108324844982787365421838248774233776150955455108880909594879354701686281508400784454018153141712714056141956102787588955423884994862476100828259602052674697911274378836670584404483343596656671559241948461934321623253684028915214150087229139562213971738267021999317602177293901813294906122800670874140719440924107506124383898499485507066575804653337392937484798873464852056622373993524920998758919649642463443
	Here is your signature:
	18039847767254078714095230144517218860563682538350048949348389043950158488173161342174400077601773971391598094658225342960430289544407969019238311191232794759869654205123261685995319184452066562228551853352401027988154730112368995219592521437335913516243409554121468796807691729260312988635424814269919709277909644088264210062313548126010758236331389478986037567397728234381532522703813907450213773972553802635871786891754532399633801802626827157141462173243560679941698077890210412109805543389280693041300919450864961331819193980272457298005765159710134284792945572867889469058910715288191378529696290994241347132914

	-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-_-^.^-

	I heard you wanted to steal my treats. You aren't worthy unless you can decrypt 818067440776360001102650781068337244336779
	Received: 6603851543688853262640421123206708703962646135673695409412410653250099873223577336554243440194371120337164201548911007194448608473166910753520059743724049331512050077440685165568213269241240109017970157263794223145238358794931272980252470460464380314500214313780465188946768709823784597225889691224839607383312707412012898040908675907483245569892356201072358121758635857345196764882649666336282403968561593040942744670696483637673225625635809658638510370739559453064158320439113141008393895924282836490932771819921707873472910277577696357028665844558613170455254772512197589: 
	Received: tjctf{cAts_4r3_d3vils_RSACRT}


## Flag

	tjctf{cAts_4r3_d3vils_RSACRT}
