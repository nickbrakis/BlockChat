from fastapi import FastAPI
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

@app.post("/transactions/new")
async def create_transaction(receiver_address : str, amount : int):
    
    # TO DO : 
    # maybe some checks??


    # 1. create a tranasaction
    # maybe we change logic to node 
    transaction = node.create_transaction()
    # 2. 