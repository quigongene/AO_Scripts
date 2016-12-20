# coding: utf-8

import base64
from ctypes import *

from . import utils


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

    v = utils.str2vec(plaintext.encode())
    k = utils.str2vec(key.encode()[:16])

    bytearray = b''.join(utils.vec2str(_encipher(chunk, k))
                         for chunk in utils.chunks(v, 2))

    return base64.b64encode(bytearray).decode()


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

    k = utils.str2vec(key.encode()[:16])
    v = utils.str2vec(base64.b64decode(ciphertext.encode()))

    return b''.join(utils.vec2str(_decipher(chunk, k))
                    for chunk in utils.chunks(v, 2)).decode()


def _encipher(v, k):
    y, z = [c_uint32(x)
            for x in v]
    sum = c_uint32(0)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]

    return [y.value, z.value]


def _decipher(v, k):
    y, z = [c_uint32(x)
            for x in v]
    sum = c_uint32(0xC6EF3720)
    delta = 0x9E3779B9

    for n in range(32, 0, -1):
        z.value -= (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        y.value -= (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        sum.value -= delta

    return [y.value, z.value]
