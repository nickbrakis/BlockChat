# pylint: disable=missing-docstring
import hashlib
import ecdsa
from pydantic import BaseModel
from wallet import Wallet


class Transaction(BaseModel):
    sender_address: str = None
    receiver_address: str = None
    type_of_transaction: str = None
    amount: float = 0
    fee: float = 0
    message: str = None
    nonce: int = 0
    signature: bytes = None
    transaction_id: str = None
    transaction_data: str = None

    def __init__(self, sender_address: str,
                 receiver_address: str,
                 type_of_transaction: str,
                 amount: float,
                 message: str,
                 nonce: int,
                 signature: bytes = None):
        super().__init__()
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.type_of_transaction = type_of_transaction
        self.fee = amount * 0.03
        self.amount = amount + self.fee
        self.message = message
        self.nonce = nonce
        self.signature = signature
        transaction_data = "{}{}{}{}{}{}".format(self.sender_address,
                                                 self.receiver_address,
                                                 self.type_of_transaction,
                                                 self.amount,
                                                 self.message,
                                                 self.nonce)
        self.transaction_id = hashlib.sha256(
            transaction_data.encode()).hexdigest()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __eq__(self, other):
        return self.transaction_id == other.transaction_id

    def sign_transaction(self, private_key: str) -> bool:
        transaction_data = "{}{}{}{}{}{}".format(self.sender_address,
                                                 self.receiver_address,
                                                 self.type_of_transaction,
                                                 self.amount,
                                                 self.message,
                                                 self.nonce)

        transaction_hash = hashlib.sha256(transaction_data.encode()).digest()
        signing_key = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        self.signature = signing_key.sign(transaction_hash).hex()

    def verify_signature(self):
        transaction_data = "{}{}{}{}{}{}".format(self.sender_address,
                                                 self.receiver_address,
                                                 self.type_of_transaction,
                                                 self.amount, self.message,
                                                 self.nonce)

        transaction_hash = hashlib.sha256(transaction_data.encode()).digest()
        verifying_key = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(self.sender_address), curve=ecdsa.SECP256k1)
        try:
            return verifying_key.verify(bytes.fromhex(self.signature), transaction_hash)
        except ecdsa.BadSignatureError:
            return False

    def validate_transaction(self, wallet: Wallet) -> tuple[str, bool]:
        if not self.verify_signature():
            return "Invalid Signature", False
        if self.receiver_address == "0":
            if not wallet.stake_check(self.amount):
                return "Failed stake check", False
            else:
                wallet.nonce += 1
                return None, True
        else:
            if not wallet.pending_balance_check(self.amount):
                return "Failed balance check", False
        if self.nonce <= wallet.nonce:
            return "Invalid nonce", False
        wallet.nonce += 1
        wallet.pending_balance -= self.amount
        return None, True

    def to_dict(self) -> dict:
        return {
            'sender_address': self.sender_address,
            'receiver_address': self.receiver_address,
            'type_of_transaction': self.type_of_transaction,
            'amount': self.amount,
            'fee': self.fee,
            'message': self.message,
            'nonce': self.nonce,
            'signature': self.signature,
            'transaction_id': self.transaction_id
        }
