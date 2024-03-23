import ecdsa
import hashlib
from blockchain import Blockchain

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

    def sign_transaction(self, private_key : str):
        transaction_data = "{}{}{}{}{}{}".format(self.sender_address, self.receiver_address, self.type_of_transaction, self.amount, self.message, self.nonce)
        transaction_hash = hashlib.sha256(transaction_data.encode()).digest()
        signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        self.signature = signing_key.sign(transaction_hash)

    def verify_signature(self):
        transaction_data = "{}{}{}{}{}{}".format(self.sender_address, self.receiver_address, self.type_of_transaction, self.amount, self.message, self.nonce)
        transaction_hash = hashlib.sha256(transaction_data.encode()).digest()
        verifying_key = ecdsa.VerifyingKey.from_string(self.sender_address, curve=ecdsa.SECP256k1)
        try:
            return verifying_key.verify(self.signature, transaction_hash)
        except ecdsa.BadSignatureError:
            return False
    
    def validate_transaction(self, blockchain : Blockchain):
        if not self.verify_signature() : 
            return False
        if not blockchain.balance_check() :
            return False
        return True