# pylint: disable=missing-docstring
from pydantic import BaseModel
import logging
import ecdsa
from fastapi import BackgroundTasks
from wallet import Wallet
from block import Block
from transaction import Transaction
from transaction_pool import TransactionPool
from blockchain import Blockchain
from broadcaster import Broadcaster

logger = logging.getLogger('uvicorn')


class Node(BaseModel):
    address: str = None
    # nodes = {public_key : wallet}
    nodes: dict[str, Wallet] = dict()
    transaction_pool: TransactionPool = TransactionPool()
    capacity: int = 5
    blockchain: Blockchain = Blockchain()
    id: int = None
    broadcaster: Broadcaster = Broadcaster()
    # for bootstrap
    gen_id: int = 0

    def __init__(self):
        super().__init__()
        self.address: str = None
        self.nodes: dict[str, Wallet] = dict()
        self.transaction_pool: TransactionPool = TransactionPool()
        self.blockchain: Blockchain = Blockchain()
        self.id = None
        self.broadcaster = Broadcaster()

    def add_node(self, node_id: int, ip: str, wallet: Wallet):
        '''Adds a node to the network.'''
        public_key = wallet.public_key
        self.broadcaster.add_node(node_id, public_key, ip)
        if wallet.private_key is not None:
            self.broadcaster.my_ip = ip
        self.nodes[public_key] = wallet

    def receive_mapping(self, mapping: dict[int, tuple[str, str]]):
        for node_id, (public_key, ip) in mapping.items():
            if public_key == self.address:
                continue
            self.add_node(node_id, ip, Wallet(public_key))

############################################################################################################
# Wallet Methods

    def get_stake(self) -> float:
        return self.nodes[self.address].stake

    def generate_private_wallet(self) -> Wallet:
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        public_key_str = private_key.get_verifying_key().to_string().hex()
        private_key_str = private_key.to_string().hex()
        return Wallet(public_key_str, private_key_str)

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
            sender.balance -= transaction.amount + transaction.fee
            receiver.balance += transaction.amount
            validator.balance += transaction.fee
        for wallet in self.nodes.values():
            wallet.pending_balance = wallet.balance

    def update_wallets_from_bootstrap(self, blockchain: Blockchain):
        for block in blockchain.blocks:
            for transaction in block.transactions:
                sender = None
                if transaction.sender_address != "0":
                    sender = self.nodes[transaction.sender_address]
                    if sender.nonce < transaction.nonce:
                        sender.nonce = transaction.nonce
                if transaction.receiver_address == "0":
                    sender.stake = transaction.amount
                    continue
                receiver = self.nodes[transaction.receiver_address]
                if sender is not None:
                    sender.balance -= transaction.amount
                receiver.balance += transaction.amount
            for wallet in self.nodes.values():
                wallet.pending_balance = wallet.balance

    def get_balance(self) -> int:
        return self.nodes[self.address].balance

    def set_stake(self, background_tasks: BackgroundTasks, amount: float) -> str:
        msg = self.create_transaction(background_tasks, "0", amount, "")
        return f"Stake set to {amount} successfully, wait for next block to be minted."

############################################################################################################
# Block & Blockchain Methods

    def view_block(self) -> Block:
        return self.blockchain.last_block()

    def receive_block(self, block: Block) -> str:
        last_hash = self.blockchain.last_block().current_hash
        ok = block.validate_block(last_hash, self.nodes)
        if not ok:
            return "Block is invalid."
        self.update_wallets(block)
        self.transaction_pool.update_from_block(block)
        self.blockchain.add_block(block)
        return f"Block {block.current_hash} added to blockchain."

    def receive_bootstrap_blockchain(self, blockchain: Blockchain):
        if len(self.blockchain.blocks) > 0:
            return "Blockchain already exists."
        self.blockchain = blockchain
        self.update_wallets_from_bootstrap(blockchain)

    def broadcast_block(self, block: Block):
        self.broadcaster.broadcast_block(block)

    def broadcast_blockchain(self, blockchain: Blockchain):
        self.broadcaster.broadcast_blockchain(blockchain)

    def mint_block(self):
        if not self.transaction_pool.is_full():
            return
        last_hash = self.blockchain.last_block().current_hash
        validator = Block.find_validator(last_hash, self.nodes)
        if validator is None:
            return
        if validator != self.address:
            return
        pending = self.transaction_pool.get_pending_transactions()
        transactions = []
        next_block = Block(previous_hash=last_hash,
                           transactions=transactions,
                           validator=self.address,
                           capacity=self.capacity)
        for _ in range(self.capacity):
            next_block.add_transaction(pending.popleft())
        next_block.validator = self.address
        self.blockchain.add_block(next_block)
        self.update_wallets(next_block)
        self.broadcast_block(next_block)

############################################################################################################
# Transaction Methods

    def broadcast_transaction(self, transaction: Transaction):
        self.broadcaster.broadcast_transaction(transaction)

    def create_transaction(self, background_tasks: BackgroundTasks, receiver_address: str, amount: float, message: str):
        if receiver_address not in self.nodes and receiver_address != "0":
            return "Invalid receiver address"

        wallet = self.nodes[self.address]
        if receiver_address == "0":
            if not wallet.stake_check(amount):
                return "Failed stake check"
        else:
            fee = amount * 0.03
            if not wallet.pending_balance_check(amount, fee):
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

        msg = self.receive_transaction(background_tasks, transaction)
        self.broadcast_transaction(transaction)
        return msg

    def receive_transaction(self, background_tasks: BackgroundTasks, transaction: Transaction):
        receiver_address = transaction.receiver_address
        sender_address = transaction.sender_address
        sender_wallet = self.nodes[sender_address]
        if receiver_address not in self.nodes and receiver_address != "0":
            return "Invalid receiver address"
        if sender_address not in self.nodes:
            return "Invalid sender address"

        msg, ok = transaction.validate_transaction(sender_wallet)
        if not ok:
            return msg

        msg, ok = self.transaction_pool.add_transaction(transaction)
        if not ok:
            return msg

        background_tasks.add_task(self.mint_block)

        return msg


############################################################################################################
# Bootstrap Methods


    def get_next_node_id(self):
        self.gen_id += 1
        return self.gen_id

    def create_gen_block(self):
        transactions = []
        gen_block = Block(
            previous_hash=1, transactions=transactions, capacity=1)
        gen_transaction = Transaction(sender_address="0",
                                      receiver_address=self.address,
                                      type_of_transaction="coins",
                                      amount=5000,
                                      message="",
                                      nonce=0)
        self.nodes[self.address].nonce += 1
        gen_block.add_transaction(gen_transaction)
        return gen_block

    async def bootstrap(self):
        self.broadcaster.broadcast_ok()
        self.broadcaster.broadcast_mapping()
        gen_block = self.create_gen_block()
        self.blockchain.add_block(gen_block)
        # transaction for each node transferring 1000 coins
        transactions = []
        next_block = Block(previous_hash=self.blockchain.last_block().current_hash,
                           transactions=transactions,
                           capacity=5)
        for node in self.nodes:
            if self.address == node:
                continue
            transaction = Transaction(sender_address=self.address,
                                      receiver_address=node,
                                      type_of_transaction="coins",
                                      amount=1000,
                                      message="",
                                      nonce=self.nodes[self.address].nonce)
            transaction.sign_transaction(
                self.nodes[self.address].get_private_key())
            self.nodes[self.address].nonce += 1
            next_block.add_transaction(transaction)

        first_stake = Transaction(sender_address=self.address,
                                  receiver_address="0",
                                  type_of_transaction="stake",
                                  amount=1,
                                  message="",
                                  nonce=self.nodes[self.address].nonce)
        first_stake.sign_transaction(
            self.nodes[self.address].get_private_key())
        self.nodes[self.address].nonce += 1
        next_block.add_transaction(first_stake)
        self.blockchain.add_block(next_block)
        self.update_wallets_from_bootstrap(self.blockchain)
        self.broadcast_blockchain(self.blockchain)
