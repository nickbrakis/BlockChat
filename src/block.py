import random
import hashlib
import time
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

class Block:
    def __init__(self, previous_hash : str, capacity : int = 10):
        self.previous_hash = previous_hash
        self.timestamp = time()
        self.current_hash : str = None
        self.index : int = None
        self.transactions : list[Transaction] = list()
        self.validator : str = None
        self.capacity : int = capacity


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

    def mint_block(self):
        pass
    
    def find_validator(self, blockchain : Blockchain) -> str:
        random.seed(blockchain.last_block().current_hash)
        validators = [validator for validator, stake in blockchain.validators.items() for _ in range(stake)]
        return random.choice(validators)
    

    def add_transaction(self, transaction : Transaction):
        self.transactions.append(transaction)