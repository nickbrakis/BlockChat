import requests
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="My Application")
    parser.add_argument("-p", "--port", help="Port in which node is running", default=8000, type=int)
    parser.add_argument("--ip", help="IP of the host", default="127.0.0.1")
    args = parser.parse_args()

    ip_address = args.ip
    port = args.port
    url = f"http://{ip_address}:{port}/"
    
    os.system("clear")
    while(True):
        print("1. Create Transaction")
        print("2. View Last Block")
        print("3. Get Balance")
        print("4. Set Stake")
        print("5. Print Hello")
        print("6. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            receiver_address = input("Enter receiver address: ")
            amount = float(input("Enter amount: "))
            message = input("Enter message: ")
            response = requests.post(
                f"{url}create_transactions/{receiver_address}/{amount}/{message}")
            print(response.json())
        elif choice == 2:
            response = requests.get(f"{url}view_last_block")
            print(response.json())
        elif choice == 3:
            response = requests.get(f"{url}balance")
            print(response.json())
        elif choice == 4:
            amount = float(input("Enter amount: "))
            response = requests.post(f"{url}set_stake/{amount}")
            print(response.json())
        elif choice == 5:
            response = requests.get(f"{url}hello")
            print(response.json())
        elif choice == 6:
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
