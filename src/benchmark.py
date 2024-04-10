# pylint: skip-file
import requests
import time
import os


def get_mapping():
    url = "http://localhost:8000/"
    mapping_string = requests.get(f"{url}get_mapping").json()
    mapping = {int(key): value for key, value in mapping_string.items()}
    return mapping


def create_transactions(nodes):
    transactions = []
    for i in range(nodes):
        with open(f'input_{nodes}/trans{i}.txt', 'r') as file:
            url = f"http://localhost:800{i}/create_transaction"
            for line in file:
                # Split the line into receiver_address and message
                node_id_str, msg = line.strip().split(' ', 1)
                node_id = int(node_id_str[2:])
                receiver_address = mapping[int(node_id)][0]
                amount = len(msg)
                message = msg

                params = {
                    "receiver_address": receiver_address,
                    "amount": amount,
                    "message": message
                }
                # Add the transaction to the list
                transactions.append((url, params))
    return transactions


def set_stakes(nodes, amount):
    for i in range(nodes):
        url = f"http://localhost:800{i}/"
        request_data = {"amount": amount}
        requests.post(f"{url}set_stake", json=request_data)


def set_superstake(node_id):
    url = f"http://localhost:800{node_id}/"
    request_data = {"amount": 100}
    requests.post(f"{url}set_stake", json=request_data)


def get_node_balance(node_id):
    url = f"http://localhost:800{node_id}/"
    response = requests.get(f"{url}balance")
    return response.json()


def execute_transactions(transactions):
    begin_time = time.time()
    for url, params in transactions:
        requests.post(url, params=params, timeout=5)
    end_time = time.time()
    total_time = end_time - begin_time
    return total_time


def get_avg_block_time():
    url = "http://localhost:8000/"
    response = requests.get(f"{url}get_avg_block_time")

    return response.json()


if __name__ == "__main__":
    experiments = [(4, 5), (4, 10), (4, 20), (9, 5), (9, 10), (9, 20)]
    output_string = ""

    for nodes, capacity in experiments:
        os.system(f"./dorun.sh {nodes} {capacity}")
        # sleep some seconds to allow the nodes to be ready
        time.sleep(5)
        mapping = get_mapping()
        set_stakes(nodes, 10)
        transactions = create_transactions(nodes)
        trans_cnt = float(len(transactions))
        total_time = execute_transactions(transactions)

        output_string += "===========================================================================\n"
        output_string += f"Benchmark: {nodes+1} nodes sending transactions with {capacity} block capacity\n"
        output_string += f"Total time : {total_time}\n"
        output_string += f"Transactions/second: {trans_cnt/total_time}\n"
        output_string += f"Avg block time: {get_avg_block_time()}\n"

    # justice benchmark
    num_nodes = 4
    for i in range(num_nodes+1):
        os.system(f"./dorun.sh 4 5")
        time.sleep(5)
        mapping = get_mapping()
        set_stakes(num_nodes, 10)
        set_superstake(1)
        transactions = create_transactions(5)
        trans_cnt = float(len(transactions))
        total_time = execute_transactions(transactions)
        output_string += "===========================================================================\n"
        output_string += f"Justice Benchmark: one node with stake 100.\n"
        for y in range(num_nodes+1):
            if y == 1:
                output_string += f"Super Stake "
            output_string += f"Node {y} balance: {get_node_balance(y)}\n"

    os.system("clear")
    print(output_string)
