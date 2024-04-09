# pylint: disable=missing-docstring
import os
import requests
import uvicorn
from fastapi import FastAPI, status, BackgroundTasks, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from blockchain import Blockchain
from transaction import Transaction
from node import Node
from block import Block
from wallet import Wallet


app = FastAPI()
node = Node()


@app.on_event("startup")
async def startup_event():
    print("Node starting up")
    ip = os.getenv("IP_ADDRESS")
    bootstrap_ip = os.getenv("BOOTSTRAP")
    wallet = node.generate_private_wallet()
    node.address = wallet.public_key
    if bootstrap_ip == ip:
        node_id = 0
        node.add_node(node_id, ip, wallet)
    else:
        print(f"Node connecting to bootstrap node at {bootstrap_ip}")
        # get node id from bootstrap node
        url = f"http://{bootstrap_ip}:8000/get_id"
        try:
            response = requests.post(url,
                                     params={"public_key": wallet.public_key,
                                             "ip": ip},
                                     timeout=10)

            node_id = response.json()["node_id"]
            # to test
            print(f'Node id :{node_id}')
            node.add_node(node_id, ip, wallet)
        except requests.exceptions.RequestException as e:
            print(f"Error when making request: {e}")


############### client/api ######################

@app.post("/create_transaction")
async def create_transaction(request: Request):
    receiver_address = request.query_params.get("receiver_address")
    amount = float(request.query_params.get("amount"))
    message = request.query_params.get("message")
    msg = node.create_transaction(receiver_address, amount, message)
    return JSONResponse(msg, status_code=status.HTTP_200_OK)


@app.get("/view_last_block")
async def view_last_block():
    last_block = node.view_block()
    block_json = last_block.model_dump_json()
    return JSONResponse(block_json, status_code=status.HTTP_200_OK)


@app.get("/balance")
async def get_balance():
    balance = node.get_balance()
    return JSONResponse(balance, status_code=status.HTTP_200_OK)


@app.get("/stake")
async def get_stake():
    stake = node.get_stake()
    return JSONResponse(stake, status_code=status.HTTP_200_OK)


@app.get("/get_mapping")
async def get_mapping():
    mapping = node.broadcaster.mapping
    mapping_json = jsonable_encoder(mapping)
    return JSONResponse(mapping_json, status_code=status.HTTP_200_OK)


@app.post("/set_stake/{amount}")
async def set_stake(amount: float):
    msg = node.set_stake(amount)
    return JSONResponse(msg, status_code=status.HTTP_200_OK)


@app.post("/receive_transaction")
async def receive_transaction(request: Request):
    data = await request.json()
    transaction = Transaction.from_dict(data)
    msg = node.receive_transaction(transaction)
    return JSONResponse(msg, status_code=status.HTTP_200_OK)


@app.post("/receive_block")
async def receive_block(request: Request):
    data = await request.json()
    block = Block.from_dict(data)
    msg = node.receive_block(block)
    return JSONResponse(msg, status_code=status.HTTP_200_OK)


@app.post("/receive_blockchain")
async def receive_blockchain(request: Request):
    data = await request.json()  # Get raw JSON from request body
    blockchain = Blockchain.from_dict(data)
    node.receive_bootstrap_blockchain(blockchain)
    return JSONResponse({"message": "Blockchain received"}, status_code=status.HTTP_200_OK)


@app.post("/receive_mapping")
async def receive_mapping(mapping: dict[int, tuple[str, str]]):
    node.receive_mapping(mapping)
    return JSONResponse({"message": "Mapping received"}, status_code=status.HTTP_200_OK)


@app.post("/get_id")
async def get_id(background_tasks: BackgroundTasks, public_key: str, ip: str):
    node_id = node.get_next_node_id()
    new_node_wallet = Wallet(public_key=public_key)
    node.add_node(node_id=node_id, ip=ip, wallet=new_node_wallet)
    print(f"Node with id {node_id} added.")

    if node_id == 4:
        background_tasks.add_task(node.bootstrap)

    return JSONResponse({"node_id": node_id}, status_code=status.HTTP_200_OK)


@app.get("/ok")
def ok():
    print("ok from some node")
    return JSONResponse({"message": "ok"}, status_code=status.HTTP_200_OK)


############ web server ######################
# handling HTTP requests
uvicorn.run(app, host="0.0.0.0", port=8000)
