# coding: utf-8
import socket

from . import tea, utils, settings


def _make_keys(secret):
    # Implementation of the diffie-helman algorithm using funcom values
    # as described here: http://aodevs.com/forums/index.php?topic=42.0

    # funcom - prime base
    dh_p = int("eca2e8c85d863dcdc26a429a71a9815ad052f6139669dd659f98ae159d313d13c6bf2838e10a69b6478b64a24bd054ba8248e8f"
               "a778703b418408249440b2c1edd28853e240d8a7e49540b76d120d3b1ad2878b1b99490eb4a2a5e84caa8a91cecbdb1aa7c816e"
               "8be343246f80c637abc653b893fd91686cf8d32d6cfe5f2a6f", 16)
    # funcom - server public key
    dh_f = int("9c32cc23d559ca90fc31be72df817d0e124769e809f936bc14360ff4bed758f260a0d596584eacbbc2b88bdd410416163e11dbf"
               "62173393fbc0c6fefb2d855f1a03dec8e9f105bbad91b3437d8eb73fe2f44159597aa4053cf788d2f9d7012fb8d7c4ce3876f7d"
               "6cd5d0c31754f4cd96166708641958de54a6def5657b9f2e92", 16)
    # funcom - generator
    dh_g = int("5", 16)

    # client secret
    dh_x = int(secret, 16)

    # dh_g = dh_g^dhx mod dh_p
    # client public key
    dh_g = pow(dh_g, dh_x, dh_p)

    # dh_k = dh_f^dhx mod dh_p ( dh_f^dhx = (dh_g^funcom hemlig nyckel)^dhx
    # shared secret used to encrypt
    dh_k = pow(dh_f, dh_x, dh_p)

    # right pad with zeroes
    return ('%016x' % dh_g)[:16], ('%016x' % dh_k)[:16]


def _make_login_token(username, password, seed):
    prefix = utils.random_hex(8)

    login_info = "|".join([username, seed, password])

    # base-4 length of login_info
    login_info_length = utils.int2str(len(login_info), base=4)

    # authentication token
    token = prefix + login_info_length + login_info

    # pad with spaces until length is a multiple of 8
    while len(token) % 8:
        token += ' '

    return token


class AOClient(object):
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key, self.public_key = _make_keys(utils.random_hex(32))
        self.server_seed = None

    def __enter__(self):
        self.connect()
        print('Connected to %s. Using seed %s.' % (settings.HOST, self.server_seed))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if self.server_seed is not None:
            return  # Already connected

        remote_ip = socket.gethostbyname(settings.HOST)
        self._sock.connect((remote_ip, settings.PORT))
        self.server_seed = self._sock.recv(1024).decode()[6:]

    def close(self):
        self._sock.shutdown(1)
        self._sock.close()
        self.server_seed = None

    def authenticate(self, username, password):
        token = _make_login_token(username, password, self.server_seed)
        cipher = tea.encrypt(token, self.private_key)
        message = "{}-{}".format(self.public_key, cipher).encode()
        self._sock.send(message)
