# pylint: skip-file
import requests
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="My Application")
    parser.add_argument("-c", "--container",
                        help="Container Number to talk to", default=0, type=int)
    args = parser.parse_args()

    port = 8000 + args.container
    url = f"http://localhost:{port}/"

    mapping_string = requests.get(f"{url}get_mapping").json()
    mapping = {int(key): value for key, value in mapping_string.items()}
    os.system("clear")
    while (True):
        balance = requests.get(f"{url}balance").json()
        print(f"Your balance is: {balance}")
        stake = requests.get(f"{url}stake").json()
        print(f"Your stake is: {stake}")
        print("\n")
        print("1. Create Transaction")
        print("2. View Last Block")
        print("3. Get Balance")
        print("4. Set Stake")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        os.system("clear")
        if choice == 1:
            print("Available nodes:")
            for key, value in mapping.items():
                print(f"Node {key}: {value[0]}")
            node_id = input("Enter node id: ")
            os.system("clear")
            receiver_address = mapping[int(node_id)][0]
            print("1. Send coins\n2. Send message\n")
            choice = int(input("Enter your choice:"))
            os.system("clear")
            if choice == 1:
                amount = float(input("Enter amount: "))
                os.system("clear")
                message = ""
            elif choice == 2:
                message = input("Enter message: ")
                os.system("clear")
                amount = len(message)
            request_data = {
                "receiver_address": receiver_address,
                "amount": amount,
                "message": message,
            }
            response = requests.post(
                f"{url}create_transaction", params=request_data)
            print(response.json())
        elif choice == 2:
            response = requests.get(f"{url}view_last_block")
            print(response.json())
        elif choice == 3:
            response = requests.get(f"{url}balance")
            print(response.json())
        elif choice == 4:
            amount = float(input("Enter amount: "))
            request_data = {"amount": amount}
            response = requests.post(
                f"{url}set_stake", json=request_data)
            print(response.json())
        elif choice == 5:
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
