# coding: utf-8

from aoclient import AOClient

if __name__ == '__main__':
    # example usage

    # Example 1
    # client = AOClient()
    # client.connect()
    # client.authenticate("username", "password")
    # client.close()

    # Example 2
    # Using a with block to open and close the connection
    # Same as above example
    with AOClient() as client:
        client.authenticate("username", "password")
