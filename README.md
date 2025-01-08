# BlockChat: A Distributed Messaging and Transaction Platform
BlockChat is a distributed messaging platform built on a simplified blockchain that provides secure and reliable messaging and transaction functionalities. It incorporates a Proof-of-Stake (PoS) consensus mechanism and simulates real-world decentralized applications by integrating cryptocurrency transactions and communication features.

## Features
1. **Wallet System**:
* Each user has a wallet containing BlockChat Coins (BCC).
* Transactions (sending coins or messages) are signed with a private key and validated with a public key.
  
2. **Blockchain Transactions**:
* **Send Coins**: Transfer coins between wallets with a 3% fee.
* **Send Messages**: Messages are charged at 1 BCC per character.
  
3. **Blockchain Network**:

* Distributed system with nodes that validate transactions and maintain the blockchain.
* Genesis block initializes the blockchain, and nodes join the network via a bootstrap node.
  
4. **Proof-of-Stake Consensus**:
* Nodes can stake coins for validation rights.
* Validators are chosen probabilistically, based on their stake.
  
5. **CLI Client**:
* Intuitive command-line interface for creating transactions, viewing balances, and interacting with the blockchain.
  
6. **Experimental Setup**:
* Performance benchmarking with different block capacities and client scales.
* Analysis of system throughput, block times, and fairness in validator selection.
