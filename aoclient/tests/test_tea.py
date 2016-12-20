# coding: utf-8
import unittest

from aoclient import tea


class TEATests(unittest.TestCase):
    def test_encryption(self):
        message = 'thisis16char'
        key = 'blahblahblahblah'

        encrypted = tea.encrypt(message, key)
        decrypted = tea.decrypt(encrypted, key)

        self.assertEquals(decrypted, message)
