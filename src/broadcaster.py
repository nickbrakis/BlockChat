class Broadcaster():
    def __init__(self):
        self.nodes_ip: dict[str, tuple[str, str]] = dict()
        self.ids_address: dict[str, str] = dict()
            

    def broadcast_block():
        pass

    def broadcast_transaction():
        pass

    def broadcast_blockchain():
        pass

    def add_node(self, public_key: str, id: str, ip: str, port: int):
        self.nodes_ip[public_key] = (ip, port)
        self.ids_address[id] = public_key