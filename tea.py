# coding: utf-8

import base64
import itertools
import math
from ctypes import *


def _str_to_ints(value):
    n = len(value)

    # Split the string into chunks
    chunk_size = math.ceil(n / 4)
    chunks = [value[chunk_size * i:chunk_size * (i + 1)]
              for i in range(4)]

    return [sum([character << 8 * j
                 for j, character in enumerate(chunk)])
            for chunk in chunks]


def _ints_to_str(vector):
    return bytes((element >> 8 * i) & 0xff
                 for element in vector
                 for i in range(4))


def _grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def encrypt(plaintext, key):
    """
    :param plaintext:
        The message to encode.  *Must* be a utf8 string and have a length which is a multiple of 8.

    :param key:
        The encryption key used to encode the plaintext message.  *Must* be a utf8 string and 16 characters long.

    :return:
        A base64 utf8 string of the encrypted message.
    """
    if not plaintext:
        return ''

    v = _str_to_ints(plaintext.encode('utf8'))
    k = _str_to_ints(key.encode('utf8')[:16])

    bytearray = b''.join(_ints_to_str(encipher(chunk, k))
                         for chunk in _grouper(2, v))

    return base64.b64encode(bytearray).decode('utf8')


def decrypt(ciphertext, key):
    """
    :param ciphertext:
        The encrypted message to decode as a base64 utf8 string.

    :param key:
        The encryption key used to encode the plaintext message.  *Must* be a utf8 string and 16 characters long.

    :return:
        A utf8 string of the decrypted message.
    """
    if not ciphertext:
        return ''

    k = _str_to_ints(key.encode('utf8')[:16])
    v = _str_to_ints(base64.b64decode(ciphertext.encode('utf8')))

    return b''.join(_ints_to_str(decipher(chunk, k))
                    for chunk in _grouper(2, v)).decode('utf8')


def encipher(v, k):
    y, z = [c_uint32(x)
            for x in v]
    sum = c_uint32(0)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]

    return [y.value, z.value]


def decipher(v, k):
    y, z = [c_uint32(x)
            for x in v]
    sum = c_uint32(0xC6EF3720)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        z.value -= (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        y.value -= (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        sum.value -= delta

    return [y.value, z.value]


def test_cast_int_str():
    i0 = b"blah blah blah blah "
    h0 = _str_to_ints(i0)
    o0 = _ints_to_str(h0)

    print('i0 = %s' % i0)
    print('h0 = %s' % h0)
    print('o0 = %s' % o0)

    i1 = [2445239922, 3778330120]
    h1 = _ints_to_str(i1)
    o1 = _str_to_ints(h1)

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
