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
        self.validator: str = self.find_validator(previous_hash, validators)
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

    def validate_block(self, last_hash: str, validators: dict[str, Wallet]) -> bool:
        if self.validator != self.find_validator(last_hash, validators):
            return False
        pending_balances = [(address, wallet.pending_balance) for address, wallet in validators.items()]
        for wallet in validators.values():
            wallet.pending_balance = wallet.balance
            
        for transaction in self.transactions:
            if not transaction.validate_transaction():
                self.reset_pending(pending_balances, validators)
                return False

        if self.current_hash != self.calculate_hash():
            self.reset_pending(pending_balances, validators)
            return False

        if self.previous_hash != last_hash:
            self.reset_pending(pending_balances, validators)
            return False
        return True
    
    def reset_pending(self, pending_balances: list[tuple[str, int]], validators: dict[str, Wallet]) -> None:
        for address, balance in pending_balances:
            validators[address].pending_balance = balance

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

    def find_validator(self, last_hash: str, validators: dict[str, Wallet]):
        random.seed(last_hash)
        validator_bag = [
            v for v, wallet in validators for _ in range(wallet.stake)]
        return random.choice(validator_bag)