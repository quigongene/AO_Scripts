# coding: utf-8
import itertools
import math
import random


def random_hex(n):
    return '%0x' % random.randrange(16 ** n)


def chunks(iterable, n):
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


def str2vec(value):
    n = len(value)

    # Split the string into chunks
    chunk_size = math.ceil(n / 4)
    chunks = [value[chunk_size * i:chunk_size * (i + 1)]
              for i in range(4)]

    return [sum([character << 8 * j
                 for j, character in enumerate(chunk)])
            for chunk in chunks]


def vec2str(vector):
    return bytes((element >> 8 * i) & 0xff
                 for element in vector
                 for i in range(4))
