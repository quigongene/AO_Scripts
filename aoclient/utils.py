# coding: utf-8
import itertools
import math
import random


def random_hex(n):
    return '%0x' % random.randrange(16 ** n)


def chunks(iterable, n):
    """
    Iterates through an iterable in chunks of size n.

    :param iterable:
        Any iterable.  Must have a length which is a multiple of n, or the last element will not contain n elements.
    :param n:
        The size of the chunks.
    :return:
        A generator that yields elements in chunks of size n.
    """
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def int2str(number, base=10):
    if number < 0:
        return '-' + int2str(-number, base)
    (d, m) = divmod(number, base)

    if d > 0:
        return int2str(d, base) + digit2char(m)

    return digit2char(m)


def digit2char(digit):
    if digit < 10:
        return str(digit)

    return chr(ord('a') + digit - 10)


def str2vec(value, l=4):
    """
    :param value:
        Encodes a binary string as a vector.  The string is split into chunks of length l and each chunk is encoded as
        2 elements in the return value.
    :param l:
        An optional length value of chunks.
    :return:
        A vector containing ceil(n / l) elements where n is the length of the value parameter.
    """
    n = len(value)

    # Split the string into chunks
    num_chunks = math.ceil(n / l)
    chunks = [value[l * i:l * (i + 1)]
              for i in range(num_chunks)]

    return [sum([character << 8 * j
                 for j, character in enumerate(chunk)])
            for chunk in chunks]


def vec2str(vector, l=4):
    """
    :param vector:
        Decodes a vector to a binary string.  The string is composed by chunks of size l for every two elements in the
        vector.
    :param l:
        The length of the chunks to compose the returned string.  This should match the value for l used by _str2vec.
        If the value used is smaller, than characters will be lost.
    :return:
    """
    return bytes((element >> 8 * i) & 0xff
                 for element in vector
                 for i in range(l)).replace(b'\x00', b'')
