# pylint: disable=missing-docstring
from transaction import Transaction
from block import Block
from pydantic import BaseModel


class TransactionPool(BaseModel):
    pending_transactions: list[Transaction] = list()
    def __init__(self):
        super().__init__()
        self.pending_transactions = list()

    def add_transaction(self, transaction: Transaction):
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
