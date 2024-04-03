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
        self.id = None

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
        self.update_wallets(block)
        self.blockchain.add_block(block)
        return f"Block {block.current_hash} added to blockchain."

    def update_wallets(self, block: Block):
        for transaction in block.transactions:
            sender = self.nodes[transaction.sender_address]
            # to prevent double spending, catch up to transaction nonce
            if sender.nonce < transaction.nonce:
                sender.nonce = transaction.nonce

            if transaction.receiver_address == "0":
                sender.stake = transaction.amount
                continue

            receiver = self.nodes[transaction.receiver_address]
            sender.balance -= transaction.amount
            receiver.balance += transaction.amount
        for wallet in self.nodes.values():
            wallet.pending_balance = wallet.balance

    def create_transaction(self, receiver_address: str, amount: int, message: str):
        if receiver_address not in self.nodes:
            return "Invalid receiver address"

        wallet = self.nodes[self.address]
        if receiver_address == "0":
            if not wallet.stake_check(amount):
                return "Failed stake check"
            else:
                return None, True
        else:
            if not wallet.pending_balance_check(amount):
                return "Failed balance check"

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
        return self.blockchain.last_block()

    def get_balance(self) -> int:
        return self.nodes[self.address].balance

    def set_stake(self, amount: int) -> str:
        self.nodes[self.address].stake = amount
        return f"Stake set to {amount} successfully."
    
    def create_gen_block(self) :
        gen_block = Block(previous_hash=1, validators=None, capacity=1) 
        gen_transaction = Transaction(sender_address=self.address,
                                      receiver_address=self.address,
                                      type_of_transaction="coins",
                                      amount=5000,
                                      message="",
                                      nonce=self.nodes[self.address].nonce)
        self.nodes[self.address].nonce += 1
        gen_block.add_transaction(gen_transaction)
        self.blockchain.add_block(gen_block)