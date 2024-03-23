import random
import hashlib
import time
from blockchain import Blockchain
from transaction import Transaction

def index_block():
    i = 0
    while True:
        yield i
        i += 1

class Block:
    def __init__(self, blockchain: Blockchain, capacity : int = 10):
        self.previous_hash = blockchain.last_block().current_hash
        self.timestamp = time()
        self.index : int = index_block()
        self.capacity : int = capacity
        random.seed(self.previous_hash)
        validators = [validator for validator, stake in blockchain.validators.items() for _ in range(stake)]
        self.validator : str = random.choice(validators)

        self.transactions : list[Transaction] = list()
        self.current_hash : str = None


    def calculate_hash(self) -> str:
        block_string = "{}{}{}{}".format(self.previous_hash, self.timestamp, self.transactions, self.validator).encode()
        return hashlib.sha256(block_string).hexdigest()
    

    def validate_block(self, blockchain : Blockchain) -> bool:
        if self.validator != self.find_validator(blockchain):
            return False

        for transaction in self.transactions:
            if not transaction.validate():
                return False

        if self.current_hash != self.calculate_hash():
            return False

        if self.previous_hash != blockchain.last_block().current_hash:
            return False
        return True         

    def add_transaction(self, transaction : Transaction):
        self.transactions.append(transaction)