# Checker
Reversing

## Challenge 

Found a flag checker program that looked pretty sketchy. Take a look at it.

file

## Solution

From the Java code, we know that ASCII is being converted to Binary String. 

Afterwhich, it goes through these methods

    public static String wow(String b, int s){
        String r = "";
        for(int x=s; x<b.length()+s; x++){
            r+=b.charAt(x%b.length());
        }
        return r;
    }
    public static String woah(String b){
        String r = "";
        for(int x=0; x<b.length(); x++){
            if(b.charAt(x)=='0')
                r+='1';
            else
                r+='0';
        }
        return r;
    }

woah() method appends the inverse of the original binary string

	woah('0110')
	=> '0110' + '1001'
	=> '01101001'

wow() method makes a rotation of the string

	wow("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 9));
	=>  'jklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi'

A stack is used, so I parsed it from the back

	Stack<Integer> t = new Stack<Integer>();

Also binary string will not pad the bits to multiples of 8

		 b+=Integer.toBinaryString(t.pop());

Hence, I had various possibilities...

---

Anyway, I put it into a Ruby script and got these answers

	Checker $ ruby solve.rb 
	Found: tjctf{quqquy813}
	Found: tjctf{quqqu9q13}
	Found: tjctf{quqqu91c3}
	Found: tjctf{quqq5sq13}
	Found: tjctf{quqq5s1c3}
	Found: tjctf{quqq53cc3}
	Found: tjctf{quq1ksq13}
	Found: tjctf{quq1ks1c3}
	Found: tjctf{quq1k3cc3}
	Found: tjctf{qu1cksq13}
	Found: tjctf{qu1cks1c3}
	Found: tjctf{qu1ck3cc3}
	Found: tjctf{q5ccksq13}
	Found: tjctf{q5ccks1c3}
	Found: tjctf{q5cck3cc3}
	Found: tjctf{1kccksq13}
	Found: tjctf{1kccks1c3}
	Found: tjctf{1kcck3cc3}

From inspection

	Found: tjctf{qu1cks1c3}

## Flag

	tjctf{qu1cks1c3}
