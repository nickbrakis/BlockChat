# pylint: disable=missing-docstring
from wallet import Wallet
from block import Block
from transaction import Transaction
from transaction_pool import TransactionPool


class Node:
    '''A node in the blockchain network. It can create transactions, receive transactions,
    broadcast transactions, view the last block, get the balance, and set the stake amount.'''

    def __init__(self):
        self.address: str = None
        self.nodes: dict[str, Wallet] = dict()
        self.transaction_pool: TransactionPool = TransactionPool()

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
        return f"Block {block.current_hash} received."

    def create_transaction(self, receiver_address: str, amount: int, message: str):
        if receiver_address not in self.nodes:
            return "Invalid receiver address"
        if self.nodes[self.address].pending_balance_check(amount):
            return "Not enough coins"

        nonce = self.nodes[self.address].get_nonce()
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
