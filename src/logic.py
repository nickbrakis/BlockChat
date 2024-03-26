from wallet import Wallet
from transaction import Transaction
from transaction_pool import TransactionPool

class Node : 
    def __init__(self):
        self.address : str = None
        self.nodes : dict[str, Wallet] = dict()
        self.transaction_pool : TransactionPool = TransactionPool()

    def add_node(self, address : str, wallet : Wallet):
        self.nodes[address] = wallet

    def bootstrap():
        pass

    def broadcast_block():
        pass

    def create_block():
        pass

    def receive_block():
        pass

    def create_transaction(self, receiver_address: str, amount: int, message: str):
        if receiver_address not in self.nodes.keys():
            return "Invalid receiver address"
        if self.nodes[self.address].pending_balance_check(amount) :
            return "Not enough coins"
        nonce  = self.nodes[self.address].get_nonce()
        transaction_type = "message" if message else "coins"
        transaction = Transaction(sender_address = self.address,
                                  receiver_address = receiver_address,
                                  amount = amount,
                                  message = message,
                                  nonce = nonce,
                                  type_of_transaction = transaction_type 
                                  )
        p_key = self.nodes[self.address].get_private_key()
        transaction.sign_transaction(p_key)

        self.receive_transaction(transaction)
        self.broadcast_transaction(transaction)
        return "Transaction Created."

    def receive_transaction(self, transaction: Transaction):
        receiver_address = transaction.receiver_address
        sender_address = transaction.sender_address
        sender_wallet = self.nodes[sender_address]
        if receiver_address not in self.nodes.keys():
            return "Invalid receiver address"
        if sender_address not in self.nodes.keys():
            return "Invalid sender address"

        msg, ok = transaction.validate_transaction(sender_wallet)
        if not ok : 
            return msg

        msg, ok = self.transaction_pool.add_transaction(transaction, sender_wallet)
        if not ok : 
            return msg
        
        return msg


    def broadcast_transaction():
        pass
    # new functions added 
    def view_block():
        pass
    
    def get_balance():
        pass

    def set_stake(amount: int):
        pass