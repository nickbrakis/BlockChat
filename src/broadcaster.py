# pylint: disable=missing-docstring
import logging
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import requests
from block import Block
from transaction import Transaction
from blockchain import Blockchain

logger = logging.getLogger('uvicorn')


class Broadcaster(BaseModel):
    mapping: dict[int, tuple[str, str]] = dict()
    my_ip: str = None

    def __init__(self):
        super().__init__()
        # self.nodes = {id, [public_key, ip]}
        self.mapping: dict[int, tuple[str, str]] = dict()
        self.my_ip: str = None

    def broadcast_block(self, block: Block):
        for _, ip in self.mapping.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:8000/receive_block"
            block_json = jsonable_encoder(block)
            requests.post(url, json=block_json, timeout=10)

    def broadcast_transaction(self, transaction: Transaction):
        for _, ip in self.mapping.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:8000/receive_transaction"
            transaction_json = jsonable_encoder(transaction)
            msg = requests.post(url, json=transaction_json, timeout=10)
            logger.info(f"Response from {ip}: {msg}")

    def broadcast_blockchain(self, blockchain: Blockchain):
        logger.info("Broadcasting blockchain")
        for _, ip in self.mapping.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:8000/receive_blockchain"
            blockchain_json = jsonable_encoder(blockchain)
            requests.post(url, json=blockchain_json, timeout=10)

    def broadcast_mapping(self):
        for _, ip in self.mapping.values():
            if ip == self.my_ip:
                continue
            url = f"http://{ip}:8000/receive_mapping"
            mapping_json = jsonable_encoder(self.mapping)
            requests.post(url, json=mapping_json, timeout=10)

    def broadcast_ok(self):
        try:
            for _, ip in self.mapping.values():
                if ip == self.my_ip:
                    continue
                url = f"http://{ip}:8000/ok"
                response = requests.get(
                    url, params={"node_ip": self.my_ip}, timeout=10)
                msg = response.json()["message"]
                if msg != "ok":
                    return False
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error when making request: {e}")
            return False

    def add_node(self, node_id: str, public_key: str, ip: str):
        self.mapping[node_id] = (public_key, ip)
