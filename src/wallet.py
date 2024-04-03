# pylint: disable=missing-docstring

class Wallet:
    '''Wallet class for the blockchain.'''

    def __init__(self, public_key: str,  private_key: str = -1, nonce: int = 0, balance: float = 0, stake: float = 0):
        self.private_key = private_key
        self.public_key = public_key
        self.nonce = nonce
        self.balance = balance
        self.stake = stake
        self.pending_balance = balance

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

    def set_stake(self, stake_amount: float) -> None:
        self.stake = stake_amount

    def get_private_key(self) -> str:
        if self.private_key == -1:
            raise ValueError("Private key is not set, wallet is public!")
        return self.private_key

    def pending_balance_check(self, amount: float):
        return self.pending_balance - self.stake >= amount

    def stake_check(self, stake_amount: float):
        return self.pending_balance >= stake_amount
