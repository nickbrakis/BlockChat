# pylint: disable=missing-docstring
from collections import deque
from transaction import Transaction
from block import Block
from pydantic import BaseModel


class TransactionPool(BaseModel):
    pending_transactions: deque[Transaction] = None
    capacity: int = 5

    def __init__(self, capacity: int = 5):
        super().__init__()
        self.pending_transactions = deque()
        self.capacity = capacity

    def add_transaction(self, transaction: Transaction):
        print(
            f"Adding transaction to pool, length = {len(self.pending_transactions)}")
        self.pending_transactions.append(transaction)
        return "Transaction Accepted", True

    def remove_transaction(self, transaction: Transaction):
        self.pending_transactions.remove(transaction)

    def get_pending_transactions(self):
        return self.pending_transactions

    def update_from_block(self, block: Block):
        for transaction in block.transactions:
            nonce = transaction.nonce
            sender_address = transaction.sender_address
            # to prevent double spending
            for pending_transaction in self.pending_transactions:
                if pending_transaction.nonce == nonce and pending_transaction.sender_address == sender_address:
                    self.pending_transactions.remove(pending_transaction)
                    break

    def is_full(self):
        return len(self.pending_transactions) >= self.capacity
