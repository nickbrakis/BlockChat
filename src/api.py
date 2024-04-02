# pylint: disable=missing-docstring
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from blockchain import Blockchain
from transaction import Transaction
from node import Node
from block import Block

app = FastAPI()

# initialize a blockchain and a node
blockchain = Blockchain()
node = Node()


############### client/api ######################

@app.post("/create_transactions/{receiver_id}/{amount}/{message}")
async def create_transaction(receiver_address: str, amount: int, message: str):
    msg = node.create_transaction(receiver_address, amount, message)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.get("/view_last_block")
async def view_last_block():
    last_block = node.view_block()
    block_json = last_block.model_dump_json()
    return JSONResponse({"block": block_json}, status_code=status.HTTP_200_OK)


@app.get("/balance")
async def get_balance():
    balance = node.get_balance()
    return JSONResponse({"balance": balance}, status_code=status.HTTP_200_OK)


@app.post("/set_stake/{amount}")
async def set_stake(amount):
    msg = node.set_stake(amount)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_transaction")
async def receive_transaction(transaction: Transaction):
    msg = node.receive_transaction(transaction)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_block")
async def receive_block(block: Block):
    msg = node.receive_block(block)
    return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)


@app.post("/receive_pair")
async def receive_pair(public_key: str, id: int,  ip: str, port: int):
    pass
