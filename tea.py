# coding: utf-8

import base64
import math
from ctypes import *


def _str_to_ints(s, r=4):
    n = len(s)
    l = math.ceil(n / r)
    return [sum([s[i * l + j] << 8 * j
                 if i * l + j < n
                 else 0
                 for j in range(l)])
            for i in range(r)]


def _ints_to_str(vector):
    return bytes((element >> 8 * i) & 0xff
                 for element in vector
                 # This needs to happen until the element is depleted
                 for i in range(4))


def encrypt(plaintext, key):
    if not plaintext:
        return ''

    v = _str_to_ints(plaintext.encode('utf8'), r=2)
    print('v = %s' % v)

    k = _str_to_ints(key.encode('utf8')[:16])
    print('k = %s' % k)

    z = encipher(v, k)

    print('encrypt = %s' % z)

    return base64.b64encode(_ints_to_str(z)).decode('utf8')


def decrypt(ciphertext, key):
    if not ciphertext:
        return ''

    v = _str_to_ints(base64.b64decode(ciphertext.encode('utf8')), r=2)
    print('v = %s' % v)

    k = _str_to_ints(key.encode('utf8')[:16])
    print('k = %s' % k)

    z = decipher(v, k)
    print('z = %s' % z)

    return _ints_to_str(z).decode('utf8')


def encipher(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0)
    delta = 0x9E3779B9
    n = 32
    w = [0, 0]

    while n > 0:
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w


def decipher(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0xC6EF3720)
    delta = 0x9E3779B9
    n = 32
    w = [0, 0]

    while n > 0:
        z.value -= (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        y.value -= (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        sum.value -= delta
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w


def test_cast_int_str():
    i0 = b"blah blah blah blah "
    h0 = _str_to_ints(i0)
    o0 = _ints_to_str(h0, l=5)

    print('i0 = %s' % i0)
    print('h0 = %s' % h0)
    print('o0 = %s' % o0)

    i1 = [2445239922, 3778330120]
    h1 = _ints_to_str(i1)
    o1 = _str_to_ints(h1, r=2)

    print('i1 = %s' % i1)
    print('h1 = %s' % h1)
    print('o1 = %s' % o1)

    assert o0 == i0
    assert o1 == i1


def test_encrypt(message, key="blahblahblahblah"):
    print('plaintext (orig) = %s ' % message)

    cipertext = encrypt(message, key)
    print('cipertext = %s ' % cipertext)

    plaintext = decrypt(cipertext, key)
    print('plaintext = %s ' % plaintext)

    assert message == plaintext
