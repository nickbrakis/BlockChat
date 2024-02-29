# from collections import OrderedDict
# import binascii
# import json

# import Crypto
# import Crypto.Random
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from Crypto.Signature import pss

# import requests
# from flask import Flask, jsonify, request, render_template

# from transaction_output import TransactionOutput


class Transaction:

    def __init__(self, sender_address, receiver_address, type_of_transaction, amount, message, nonce, transaction_id=None, signature=None):
        """Inits a Transaction"""
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        self.amount = amount
        self.message = message
        self.nonce = nonce
        self.transaction_id = transaction_id
        self.signature = signature

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        return self.transaction_id == other.transaction_id

    def sign_transaction(self, private_key):
        pass

    def verify_signature(self):
        pass
    
    def validate_transaction(self):
        pass