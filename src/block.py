# pylint: disable=missing-docstring
import random
import hashlib
import time
from pydantic import BaseModel
from transaction import Transaction
from wallet import Wallet

import logging

logger = logging.getLogger('uvicorn')


class Block(BaseModel):
    previous_hash: str = None
    validator: str = None
    capacity: int = 10
    transactions: list[Transaction] = None
    timestamp: int = None
    index: int = None
    current_hash: str = None

    def __init__(self, previous_hash: str,
                 capacity: int = 10,
                 validator: str = None,
                 transactions: list[Transaction] = [],
                 timestamp: int = int(time.time()),
                 index: int = next(i for i in range(1, 1000000)),
                 current_hash: str = None):
        super().__init__()
        self.previous_hash: str = previous_hash
        self.capacity: int = capacity
        self.validator: str = validator
        self.transactions: list[Transaction] = transactions
        self.timestamp: int = timestamp
        self.index: int = index
        self.current_hash: str = current_hash

    @classmethod
    def from_dict(cls, data: dict):
        previous_hash = data.get('previous_hash')
        capacity = data.get('capacity')
        validator = data.get('validator')
        transactions_dict = data.get('transactions')
        transactions = []
        for t_dict in transactions_dict:
            transactions.append(Transaction.from_dict(t_dict))
        timestamp = data.get('timestamp')
        index = data.get('index')
        current_hash = data.get('current_hash')
        return cls(previous_hash, capacity, validator, transactions, timestamp, index, current_hash)

    def calculate_hash(self) -> str:
        transactions_str = ""
        for transaction in self.transactions:
            transactions_str += transaction.to_string()
        block_string = "{}{}{}".format(self.previous_hash,
                                       transactions_str,
                                       self.validator).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_block(self, last_hash: str, validators: dict[str, Wallet]) -> bool:
        if self.validator != self.find_validator(last_hash, validators):
            logger.error(" ERR1 Invalid Validator!")
            return False
        pending_balances = [(address, wallet.pending_balance)
                            for address, wallet in validators.items()]
        for wallet in validators.values():
            wallet.pending_balance = wallet.balance

        for transaction in self.transactions:
            sender = validators[transaction.sender_address]
            if not transaction.validate_transaction(sender):
                logger.error("Invalid Transaction!")
                self.reset_pending(pending_balances, validators)
                logger.error(" ERR2 Invalid Transaction!")
                return False

        if self.current_hash != self.calculate_hash():
            logger.error("Invalid Hash!")
            logger.error(f"Expected: {self.calculate_hash()}")
            logger.error(f"Actual: {self.current_hash}")
            self.reset_pending(pending_balances, validators)
            return False

        if self.previous_hash != last_hash:
            logger.error("ERR 3 Invalid Previous Hash!")
            self.reset_pending(pending_balances, validators)
            return False
        return True

    def reset_pending(self, pending_balances: list[tuple[str, int]], validators: dict[str, Wallet]) -> None:
        for address, balance in pending_balances:
            validators[address].pending_balance = balance

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    @staticmethod
    def find_validator(last_hash: str, validators: dict[str, Wallet]):
        random.seed(last_hash)
        # on bootstrap, validators is None
        if validators is not None and validators != {}:
            validator_bag = [
                v for v, wallet in validators.items() for _ in range(int(wallet.stake))]
        else:
            validator_bag = []
        if validator_bag == []:
            return None
        # sort the validator bag to ensure same choice amongst nodes
        validator_bag.sort()
        return random.choice(validator_bag)
