# coding: utf-8

from aoclient import AOClient

if __name__ == '__main__':
    # example usage

    with AOClient() as client:
        client.authenticate("username", "password")
