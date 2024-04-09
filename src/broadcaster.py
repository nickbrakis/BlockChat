# pylint: disable=missing-docstring
from pydantic import BaseModel
import requests
from block import Block
from transaction import Transaction
from blockchain import Blockchain


class Broadcaster(BaseModel):
    # nodes = {id, [public_key, ip, port]}
    nodes: dict[int, tuple[str, str, str]] = dict()
    my_ip: str = None

    def __init__(self):
        super().__init__()
        self.nodes: dict[int, tuple[str, str, str]] = dict()
        self.my_ip: str = None

    def broadcast_block(self, block: Block):
        for _, ip, port in self.nodes.values():
            url = f"http://{ip}:{port}/receive_block"
            block_json = block.model_dump_json()
            requests.post(url, json=block_json, timeout=10)

    def broadcast_transaction(self, transaction: Transaction):
        for _, ip, port in self.nodes.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:{port}/receive_transaction"
            transaction_json = transaction.model_dump_json()
            requests.post(url, json=transaction_json, timeout=10)

    def broadcast_blockchain(self, blockchain: Blockchain):
        for _, ip, port in self.nodes.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:{port}/receive_blockchain"
            blockchain_json = blockchain.model_dump_json()
            requests.post(url, json=blockchain_json, timeout=10)

    def broadcast_mapping(self):
        for _, ip, port in self.nodes.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:{port}/receive_mapping"
            requests.post(url, json=self.nodes, timeout=10)

    def broadcast_ok(self):
        try:
            for _, ip, port in self.nodes.values():
                if ip == self.my_ip:
                    continue
                url = f"http://{ip}:{port}/ok"
                response = requests.get(
                    url, params={"node_ip": self.my_ip}, timeout=10)
                msg = response.json()["message"]
                if msg is not "ok":
                    return False
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error when making request: {e}")
            return False

    def add_node(self, node_id: str, public_key: str, ip: str, port: int):
        self.nodes[node_id] = (public_key, ip, port)
