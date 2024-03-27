# pylint: disable=missing-docstring
from wallet import Wallet
from block import Block
from transaction import Transaction
from transaction_pool import TransactionPool
from blockchain import Blockchain

class Node:
    def __init__(self):
        self.address: str = None
        self.nodes: dict[str, Wallet] = dict()
        self.transaction_pool: TransactionPool = TransactionPool()
        self.blockchain: Blockchain = Blockchain()

    def add_node(self, address: str, wallet: Wallet):
        '''Adds a node to the network.'''
        self.nodes[address] = wallet

    def bootstrap(self):
        pass

    def broadcast_block(self):
        pass

    def create_block(self):
        pass


    def receive_block(self, block: Block) -> str:
        last_hash = self.blockchain.last_block().current_hash
        ok = block.validate_block(last_hash, self.nodes)
        if not ok:
            return "Block is invalid."
        # TO DO : make validators rewards
        self.update_balances(block)
        self.blockchain.add_block(block)
        return f"Block {block.current_hash} added to blockchain."
    
    def update_balances(self, block: Block):
        for transaction in block.transactions:
            sender = self.nodes[transaction.sender_address]
            receiver = self.nodes[transaction.receiver_address]
            sender.balance -= transaction.amount
            receiver.balance += transaction.amount
        for wallet in self.nodes.values():
            wallet.pending_balance = wallet.balance

    def create_transaction(self, receiver_address: str, amount: int, message: str):
        if receiver_address not in self.nodes:
            return "Invalid receiver address"
        if self.nodes[self.address].pending_balance_check(amount):
            return "Not enough coins"

        nonce = self.nodes[self.address].nonce
        transaction_type = "message" if message else "coins"
        transaction = Transaction(sender_address=self.address,
                                  receiver_address=receiver_address,
                                  amount=amount,
                                  message=message,
                                  nonce=nonce,
                                  type_of_transaction=transaction_type
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
        if receiver_address not in self.nodes:
            return "Invalid receiver address"
        if sender_address not in self.nodes:
            return "Invalid sender address"

        msg, ok = transaction.validate_transaction(sender_wallet)
        if not ok:
            return msg

        msg, ok = self.transaction_pool.add_transaction(
            transaction, sender_wallet)
        if not ok:
            return msg

        return msg

    def broadcast_transaction(self, transaction: Transaction):
        pass

    def view_block(self) -> Block:
        '''Returns the last block of the blockchain'''
        pass

    def get_balance(self) -> int:
        '''Returns the balance of the current node'''
        return 0

    def set_stake(self, amount: int) -> str:
        return f"Stake set to {amount} successfully."
