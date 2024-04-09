# pylint: disable=missing-docstring
import random
import hashlib
import time
from pydantic import BaseModel
from transaction import Transaction
from wallet import Wallet


index_generator = ()


class Block(BaseModel):
    previous_hash: str = None
    validators: dict[str, Wallet] = dict()
    validator: str = None
    capacity: int = 10
    transactions: list[Transaction] = list()
    timestamp: int = None
    index: int = None
    current_hash: str = None

    def __init__(self, previous_hash: str,
                 validators: dict[str, Wallet],
                 capacity: int = 10,
                 transactions: list[Transaction] = list(),
                 timestamp: int = int(time.time()),
                 index: int = next(i for i in range(1, 1000000)),
                 current_hash: str = None):
        super().__init__()
        self.previous_hash: str = previous_hash
        self.capacity: int = capacity
        self.validator: str = self.find_validator(previous_hash, validators)
        self.transactions: list[Transaction] = transactions
        self.timestamp: int = timestamp
        self.index: int = index
        if current_hash is None:
            self.current_hash: str = self.calculate_hash()
        else:
            self.current_hash: str = current_hash

    @classmethod
    def from_dict(cls, data: dict):
        previous_hash = data.get('previous_hash')
        validators_dict = data.get('validators')
        validators = dict()
        for address, wallet_dict in validators_dict.items():
            validators[address] = Wallet.from_dict(wallet_dict)
        capacity = data.get('capacity')
        transactions_dict = data.get('transactions')
        transactions = []
        for t_dict in transactions_dict:
            transactions.append(Transaction.from_dict(t_dict))
        timestamp = data.get('timestamp')
        index = data.get('index')
        current_hash = data.get('current_hash')
        return cls(previous_hash, validators, capacity, transactions, timestamp, index, current_hash)

    def calculate_hash(self) -> str:
        block_string = "{}{}{}{}".format(self.previous_hash,
                                         self.timestamp,
                                         self.transactions,
                                         self.validator).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_block(self, last_hash: str, validators: dict[str, Wallet]) -> bool:
        if self.validator != self.find_validator(last_hash, validators):
            return False
        pending_balances = [(address, wallet.pending_balance)
                            for address, wallet in validators.items()]
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

    def find_validator(self, last_hash: str, validators: dict[str, Wallet]):
        random.seed(last_hash)
        # on bootstrap, validators is None
        if validators is not None:
            validator_bag = [
                v for v, wallet in validators for _ in range(wallet.stake)]
        else:
            validator_bag = []
        if validator_bag == []:
            return None
        return random.choice(validator_bag)
