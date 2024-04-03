# pylint: disable=missing-docstring
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import requests
from blockchain import Blockchain
from transaction import Transaction
from node import Node
from block import Block
import os


app = FastAPI()
node = Node()
i_am_bootstrap = False


@app.on_event("startup")
def startup_event():
    ip = os.getenv("IP_ADDRESS")
    port = os.getenv("PORT")
    bootstrap_ip = os.getenv("BOOTSTRAP")
    bootstrap_port = os.getenv("BOOTSTRAP_PORT")
    wallet = node.generate_private_wallet()
    if bootstrap_ip == ip and bootstrap_port == port:
        node_id = 0
        global i_am_bootstrap
        i_am_bootstrap = True
    else:
        # get node id from bootstrap node
        url = f"http://{bootstrap_ip}:{bootstrap_port}/get_id"
        response = requests.post(
            url, json={"public_key": wallet.public_key, "ip": ip, "port": port})
        node_id = response.json()["node_id"]
    node.add_node(node_id, ip, port, wallet)


############### client/api ######################

@app.post("/create_transactions/{receiver_id}/{amount}/{message}")
def create_transaction(receiver_address: str, amount: float, message: str):
    msg = node.create_transaction(receiver_address, amount, message)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.get("/view_last_block")
def view_last_block():
    last_block = node.view_block()
    block_json = last_block.model_dump_json()
    return JSONResponse(block_json, status_code=status.HTTP_200_OK)


@app.get("/balance")
def get_balance():
    balance = node.get_balance()
    return JSONResponse({"balance": balance}, status_code=status.HTTP_200_OK)


@app.post("/set_stake/{amount}")
def set_stake(amount: float):
    msg = node.set_stake(amount)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_transaction")
def receive_transaction(transaction: Transaction):
    msg = node.receive_transaction(transaction)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_block")
def receive_block(block: Block):
    msg = node.receive_block(block)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_blockchain")
def receive_blockchain(blockchain: Blockchain):
    node.blockchain = blockchain
    return JSONResponse({"message": "Blockchain received"}, status_code=status.HTTP_200_OK)


@app.post("/receive_mapping")
def receive_mapping(mapping: dict[int, tuple[str, str, str]]):
    node.broadcaster.nodes = mapping
    return JSONResponse({"message": "Mapping received"}, status_code=status.HTTP_200_OK)


@app.post("/get_id")
def get_id(public_key: str, ip: str, port: int):
    node_id = node.get_next_node_id()
    node.add_node(node_id, public_key, ip, port)
    return JSONResponse({"node_id": node_id}, status_code=status.HTTP_200_OK)
