# pylint: disable=missing-docstring
import json
import requests
from block import Block
from transaction import Transaction
from blockchain import Blockchain
from pydantic import BaseModel


class Broadcaster(BaseModel):
    # nodes = {id, [public_key, ip, port]}
    nodes: dict[int, tuple[str, str, str]] = dict()
    def __init__(self):
        super().__init__()
        self.nodes: dict[int, tuple[str, str, str]] = dict()

    def broadcast_block(self, block: Block):
        for _, ip, port in self.nodes.values():
            url = f"http://{ip}:{port}/receive_block"
            block_json = block.model_dump_json()
            requests.post(url, json=block_json, timeout=10)

    def broadcast_transaction(self, transaction: Transaction):
        for _, ip, port in self.nodes.values():
            url = f"http://{ip}:{port}/receive_transaction"
            transaction_json = transaction.model_dump_json()
            requests.post(url, json=transaction_json, timeout=10)

    def broadcast_blockchain(self, blockchain: Blockchain):
        for _, ip, port in self.nodes.values():
            url = f"http://{ip}:{port}/receive_blockchain"
            blockchain_json = blockchain.model_dump_json()
            requests.post(url, json=blockchain_json, timeout=10)

    def broadcast_mapping(self):
        for _, ip, port in self.nodes.values():
            url = f"http://{ip}:{port}/receive_mapping"
            requests.post(url, json=self.nodes, timeout=10)

    def add_node(self, node_id: str, public_key: str, ip: str, port: int):
        self.nodes[node_id] = (public_key, ip, port)
