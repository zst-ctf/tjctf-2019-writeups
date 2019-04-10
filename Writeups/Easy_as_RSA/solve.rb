#!/usr/bin/env ruby
require 'openssl'

# From challenge
n = 379557705825593928168388035830440307401877224401739990998883
e = 65537
c = 29031324384546867512310480993891916222287719490566042302485

# Factorised by factordb.com
p = 564819669946735512444543556507
q = 671998030559713968361666935769

raise "wrong factors" unless p*q == n

# Helper methods
"""
def extended_gcd(a, b)
  last_remainder, remainder = a.abs, b.abs
  x, last_x, y, last_y = 0, 1, 1, 0
  while remainder != 0
    last_remainder, (quotient, remainder) = remainder, last_remainder.divmod(remainder)
    x, last_x = last_x - quotient*x, x
    y, last_y = last_y - quotient*y, y
  end
 
  return last_remainder, last_x * (a < 0 ? -1 : 1)
end
 
def invmod(e, et)
  g, x = extended_gcd(e, et)
  if g != 1
    raise 'The maths are broken!'
  end
  x % et
end
"""

def invmod(e, et)
  e.to_bn.mod_inverse(et)
end

def powmod(x, e, n)
  x.to_bn.mod_exp(e, n)
end

def hex2ascii(text)
  [text].pack('H*')
end

# Decrypt
phi = (p-1)*(q-1)
d = invmod(e,phi)

plaintext = powmod(c, d, n)
plaintext = plaintext.to_s(16)
plaintext = hex2ascii(plaintext)
puts plaintext
