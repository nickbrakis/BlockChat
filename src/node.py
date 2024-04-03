# pylint: disable=missing-docstring
import ecdsa
from wallet import Wallet
from block import Block
from transaction import Transaction
from transaction_pool import TransactionPool
from blockchain import Blockchain
from broadcaster import Broadcaster


class Node:
    def __init__(self):
        self.address: str = None
        self.nodes: dict[str, Wallet] = dict()
        self.transaction_pool: TransactionPool = TransactionPool()
        self.blockchain: Blockchain = Blockchain()
        self.id = None
        self.broadcaster = Broadcaster()

    def generate_private_wallet(self) -> Wallet:
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key_str = private_key.get_verifying_key().to_string().hex()
        private_key_str = private_key.to_string().hex()
        return Wallet(public_key_str, private_key_str)

    def add_node(self, node_id: int, ip: str, port: int, wallet: Wallet):
        '''Adds a node to the network.'''
        public_key = wallet.public_key
        self.broadcaster.add_node(node_id, public_key, ip, port)
        self.nodes[public_key] = wallet

    def broadcast_block(self, block: Block):
        self.broadcaster.broadcast_block(block)

    def broadcast_transaction(self, transaction: Transaction):
        self.broadcaster.broadcast_transaction(transaction)

    def broadcast_blockchain(self, blockchain: Blockchain):
        self.broadcaster.broadcast_blockchain(blockchain)

    def receive_block(self, block: Block) -> str:
        last_hash = self.blockchain.last_block().current_hash
        ok = block.validate_block(last_hash, self.nodes)
        if not ok:
            return "Block is invalid."
        self.update_wallets(block)
        self.blockchain.add_block(block)
        return f"Block {block.current_hash} added to blockchain."

    def update_wallets(self, block: Block):
        validator = self.nodes[block.validator]
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
            receiver.balance += transaction.amount - transaction.fee
            validator.balance += transaction.fee
        for wallet in self.nodes.values():
            wallet.pending_balance = wallet.balance

    def create_transaction(self, receiver_address: str, amount: float, message: str):
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

        msg, ok = self.transaction_pool.add_transaction(transaction)
        if not ok:
            return msg

        return msg

    def view_block(self) -> Block:
        return self.blockchain.last_block()

    def get_balance(self) -> int:
        return self.nodes[self.address].balance

    def set_stake(self, amount: float) -> str:
        self.nodes[self.address].stake = amount
        return f"Stake set to {amount} successfully."

    def create_gen_block(self):
        gen_block = Block(previous_hash=1, validators=None, capacity=1)
        gen_transaction = Transaction(sender_address="0",
                                      receiver_address=self.address,
                                      type_of_transaction="coins",
                                      amount=5000,
                                      message="",
                                      nonce=self.nodes[self.address].nonce)
        self.nodes[self.address].nonce += 1
        gen_block.add_transaction(gen_transaction)
        return gen_block

    def get_next_node_id(self):
        idx = 1
        while True:
            yield idx
            idx += 1

    def bootstrap(self):
        self.broadcaster.broadcast_mapping()
        gen_block = self.create_gen_block()
        self.blockchain.add_block(gen_block)
        self.broadcast_blockchain(self.blockchain)
        # transaction for each node tranferring 1000 coins
        for node in self.nodes:
            if self.address == node:
                continue
            transaction = Transaction(sender_address=self.address,
                                      receiver_address=node,
                                      type_of_transaction="coins",
                                      amount=1000,
                                      message="",
                                      nonce=self.nodes[self.address].nonce)
            self.nodes[self.address].nonce += 1
            self.receive_transaction(transaction)
            self.broadcast_transaction(transaction)
