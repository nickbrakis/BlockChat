from fastapi import FastAPI
from pydantic import BaseModel
import json
import argparse

from wallet import Wallet
from blockchain import Blockchain
from transaction import Transaction

app = FastAPI()

blockchain = Blockchain()

# client/api
@app.post("/transactions/new")
async def create_transaction(transaction: Transaction):
    index = blockchain.new_transaction(transaction.sender, transaction.recipient, transaction.amount)
    return {"message": f"Transaction will be added to Block {index}"}

