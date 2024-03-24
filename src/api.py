from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import argparse

from wallet import Wallet
from blockchain import Blockchain
from transaction import Transaction
from logic import Node

app = FastAPI()

# initialize a blockchain and a node
blockchain = Blockchain()
node = Node()


############### client/api ######################

@app.post("/create_transactions/{receiver_id}/{amount}")
async def create_transaction(receiver_address: str, amount: int):
    # TO DO : 
    # maybe some checks??

    # 1. create a transaction and add to pending transactions
    # maybe we change logic to node 
    transaction = node.create_transaction(receiver_address, amount)
    # 2. broadcast the transaction 
    node.broadcast_transaction(transaction)

    return JSONResponse("Transaction created and broadcasted successfully", status_code=status.HTTP_200_OK)

@app.get("/view_last_block")
async def view_last_block():
    # view block function of backend returns last block
    last_block = node.view_block()
    transactions_list = last_block.transactions
    validator_id = last_block.validator
    
    transactions = []
    for transaction in transactions_list:
        transactions.append(
            {
                "sender_id": node.ring[transaction.sender_address]['id'],
                # "sender_address": transaction.sender_address,
                "receiver_id": node.ring[transaction.receiver_address]['id'],
                # "receiver_address": transaction.receiver_address,
                "amount": transaction.amount
            }
        )
    transactions.append({"validator" : validator_id})

    return JSONResponse(transactions, status_code=status.HTTP_200_OK)

@app.get("/balance")
async def get_balance():
    balance = node.get_balance()
    return JSONResponse({"balance": balance}, status_code=status.HTTP_200_OK)


@app.post("/set_stake/{amount}")
async def set_stake(amount):
    node.set_stake(amount)
    return JSONResponse(f"Stake set to {amount}", status_code=status.HTTP_200_OK)