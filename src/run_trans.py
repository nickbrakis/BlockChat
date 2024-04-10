import requests
import time

transactions = []
url = "http://localhost:8000/"
mapping_string = requests.get(f"{url}get_mapping").json()
mapping = {int(key): value for key, value in mapping_string.items()}


for i in range(5):
    with open(f'input/trans{i}.txt', 'r') as file:
        url = f"http://localhost:800{i}/"
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
    response = requests.post(url, params=params, timeout = 5)

end_time = time.time()

print(f"Total time : {end_time - begin_time}")
print(f"Transactions/second: {trans_cnt/(end_time - begin_time)}")