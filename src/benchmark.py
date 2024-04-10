import requests
import time
import os

experiments = [(4, 5), (4, 10), (4, 20), (9, 5), (9, 10), (9, 20)]
output_string = ""
for nodes, capacity in experiments:
    # call ./dorun.sh 5 to start 5 nodes and wait for them to be ready
    os.system(f"./dorun.sh {nodes} {capacity}")
    # sleep seconds to allow the nodes to be ready
    time.sleep(5)
    transactions = []
    url = "http://localhost:8000/"
    mapping_string = requests.get(f"{url}get_mapping").json()
    mapping = {int(key): value for key, value in mapping_string.items()}
    n = 5

    for i in range(n):
        with open(f'input_{n}/trans{i}.txt', 'r') as file:
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

    begin_time = time.time()
    trans_cnt = float(len(transactions))

    for url, params in transactions:
        response = requests.post(url, params=params, timeout=5)

    end_time = time.time()
    output_string += "===========================================================================\n"
    output_string += f"Benchmark: {nodes} nodes sending transactions with {capacity} block capacity\n"
    output_string += f"Total time : {end_time - begin_time}\n"
    output_string += f"Transactions/second: {trans_cnt/(end_time - begin_time)}\n"

os.system("clear")
print(output_string)
