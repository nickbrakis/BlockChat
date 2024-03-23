class Wallet:

    def __init__(self, public_key : str,  private_key:str = -1 , nonce : int = 0, balance : int = 0, stake : int = 0):
        self.private_key = private_key
        self.public_key = public_key
        self.nonce = nonce
        self.balance = balance
        self.stake = stake

    def __str__(self) -> str:
        """Returns a string representation of a Wallet object."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def get_balance(self) -> int:
        return self.balance

    def set_stake(self, stake_amount: int) -> None:
        self.stake = stake_amount

    def get_address(self) -> str:
        return self.public_key
    
    def get_private_key(self) -> str:
        if self.private_key == -1:
            raise Exception("Private key is not set, wallet is public!")
        return self.private_key

    def get_nonce(self):
        while True:
            yield self.nonce
            self.nonce += 1
