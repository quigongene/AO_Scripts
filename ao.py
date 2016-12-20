# coding: utf-8
import random

import tea


def _random_hex(n):
    return '%0x' % random.randrange(16 ** n)


def _digit_to_char(digit):
    if digit < 10:
        return str(digit)

    return chr(ord('a') + digit - 10)


def _str_base(number, base):
    if number < 0:
        return '-' + _str_base(-number, base)
    (d, m) = divmod(number, base)

    if d > 0:
        return _str_base(d, base) + _digit_to_char(m)

    return _digit_to_char(m)


def generate_ao_token(seed, username, password):
    prefix = _random_hex(8)

    login_info = "{username}|{seed}|{password}".format(
        username=username,
        seed=seed,
        password=password
    )

    # base-4 length of login_info
    login_info_length = _str_base(len(login_info), 4)

    # authentication token
    token = prefix + login_info_length + login_info

    # pad with spaces until length is a multiple of 8
    while len(token) % 8:
        token += ' '

    return token


def ao_tea_keys():
    # prime base
    dhN = int("eca2e8c85d863dcdc26a429a71a9815ad052f6139669dd659f98ae159d313d13c6bf2838e10a69b6478b64a24bd054ba8248e8fa"
              "778703b418408249440b2c1edd28853e240d8a7e49540b76d120d3b1ad2878b1b99490eb4a2a5e84caa8a91cecbdb1aa7c816e8b"
              "e343246f80c637abc653b893fd91686cf8d32d6cfe5f2a6f", 16)

    # public key
    dhY = int("9c32cc23d559ca90fc31be72df817d0e124769e809f936bc14360ff4bed758f260a0d596584eacbbc2b88bdd410416163e11dbf6"
              "2173393fbc0c6fefb2d855f1a03dec8e9f105bbad91b3437d8eb73fe2f44159597aa4053cf788d2f9d7012fb8d7c4ce3876f7d6c"
              "d5d0c31754f4cd96166708641958de54a6def5657b9f2e92", 16)

    dhG = int("5", 16)

    # Random 256 bit number
    # secret key
    rndhex = int(_random_hex(32), 16)

    # dhX = dhG^dhx modulo dhN
    # public key
    dhX = dhG ** rndhex % dhN

    # dhK = dhY^dhx modulo dhN ( dhY^dhx = (dhG^funcom hemlig nyckel)^dhx
    # shared secret used to encrypt
    dhK = dhY ** rndhex % dhN

    # right pad with zeroes
    return ('%016x' % dhX)[:16], ('%016x' % dhK)[:16]


request = generate_ao_token(1234, 'username', 'pass')
public, private = ao_tea_keys()
encrypted = tea.encipher(request, private)

print("{public_key}-{message}".format(public_key=public, message=encrypted))
