from transaction import Transaction
from blockchain import Blockchain

class TransactionPool:
    def __init__(self, blockchain: Blockchain):
        self.pending_transactions = list()
        self.blockchain = blockchain
        self.pending_balance = dict()
        for address, wallet in blockchain.validators.items():
            self.pending_balance[address] = wallet.get_balance()

    def add_transaction(self, transaction : Transaction):
        # check for nonce before adding
        for t in self.pending_transactions:
            if t.sender_address == transaction.sender_address and t.nonce == transaction.nonce:
                return
        if transaction.amount < self.pending_balance[transaction.sender_address]:
            self.pending_balance[transaction.sender_address] -= transaction.amount
            self.pending_transactions.append(transaction)
        
    
    def remove_transaction(self, transaction : Transaction):
        self.pending_transactions.remove(transaction)
    
    def get_pending_transactions(self):
        return self.pending_transactions
    
    def balance_check(self, sender_address : str, amount : int) -> bool:
        return self.pending_balance[sender_address] >= amount