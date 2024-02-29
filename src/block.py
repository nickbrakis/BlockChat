# BLOCK 
########################
##
# import json
# from dotenv import load_dotenv
# import os

# from time import time
# from Crypto.Hash import SHA256

# from transaction import Transaction
# from blockchain import Blockchain

# load_dotenv()
# block_size = int(os.getenv('BLOCK_SIZE'))
# mining_difficulty = int(os.getenv('MINING_DIFFICULTY'))

class Block:
    def __init__(self, previous_hash):
        """
        Initialize a block
        """
        self.previous_hash = previous_hash
        self.timestamp = time()
        self.current_hash = None
        self.index = None
        self.transactions = []
        self.validator = None
	
    def calculate_hash(self):
        pass
    
    def validate_block(self):
        pass        

    def mint_block(self):
        pass
    
    def __find_validator(self):
        pass

    def add_transaction(self, transaction):
        self.transactions.append(transaction)