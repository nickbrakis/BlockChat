from transaction import Transaction
from blockchain import Blockchain
from wallet import Wallet

class TransactionPool:
    def __init__(self):
        self.pending_transactions = list()

    def add_transaction(self, transaction: Transaction, wallet: Wallet):
        if transaction.nonce <= wallet.nonce:
            return "Invalid nonce", False
        wallet.nonce += 1
        self.pending_transactions.append(transaction)
        return "Transaction Accepted", True
    
    def remove_transaction(self, transaction : Transaction):
        self.pending_transactions.remove(transaction)
    
    def get_pending_transactions(self):
        return self.pending_transactions
