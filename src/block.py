# pylint: disable=missing-docstring
import random
import hashlib
import time
from pydantic import BaseModel
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet


def index_block():
    i = 0
    while True:
        yield i
        i += 1


class Block(BaseModel):
    def __init__(self, previous_hash: str, validators: dict[str, Wallet], capacity: int = 10):
        super().__init__()
        self.previous_hash: str = previous_hash
        self.capacity: int = capacity

        random.seed(self.previous_hash)
        validator_bag = [
            v for v, wallet in validators for _ in range(wallet.stake)]
        self.validator: str = random.choice(validator_bag)

        self.transactions: list[Transaction] = list()
        self.timestamp: int = int(time.time())
        self.index: int = index_block()
        self.current_hash: str = None

    def calculate_hash(self) -> str:
        block_string = "{}{}{}{}".format(self.previous_hash,
                                         self.timestamp,
                                         self.transactions,
                                         self.validator).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_block(self, blockchain: Blockchain) -> bool:
        if self.validator != self.find_validator(blockchain):
            return False

        for transaction in self.transactions:
            if not transaction.validate_transaction():
                return False

        if self.current_hash != self.calculate_hash():
            return False

        if self.previous_hash != blockchain.last_block().current_hash:
            return False
        return True

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def to_json(self) -> dict:
        transactions_list = self.transactions
        validator_id = self.validator

        transactions = []
        for transaction in transactions_list:
            transactions.append(
                {
                    "sender_id": transaction.sender_address,
                    "receiver_id": transaction.receiver_address,
                    "amount": transaction.amount
                }
            )
        transactions.append({"validator": validator_id})
