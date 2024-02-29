# import binascii

# import Crypto
# import Crypto.Random
# from Crypto.Hash import SHA
# from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5

# import hashlib
# import json
# from time import time
# from urllib.parse import urlparse
# from uuid import uuid4

# from json import JSONEncoder


class Wallet:


    def __init__(self):
        """Inits a Wallet"""
        # Generate a private key of key length of 1024 bits.
        key = RSA.generate(1024)

        self.private_key = key.exportKey().decode('ISO-8859-1')
        # Generate the public key from the above private key.
        self.public_key = key.publickey().exportKey().decode('ISO-8859-1')
        self.nonce = 0
        self.balance = 0
        self.stake = 0

    def __str__(self):
        """Returns a string representation of a Wallet object."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def get_balance(self):
        pass

    def stake(self, amount):
        pass