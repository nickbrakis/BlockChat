# pylint: disable=missing-docstring
from pydantic import BaseModel


class Wallet(BaseModel):
    '''Wallet class for the blockchain.'''
    public_key: str = None
    private_key: str = -1
    nonce: int = 0
    balance: float = 0
    stake: float = 0
    pending_balance: float = 0

    def __init__(self, public_key: str,  private_key: str = None, nonce: int = 0, balance: float = 0, stake: float = 0):
        super().__init__()
        self.private_key = private_key
        self.public_key = public_key
        self.nonce = nonce
        self.balance = balance
        self.stake = stake
        self.pending_balance = balance

    @classmethod
    def from_dict(cls, data: dict):
        public_key = data.get('public_key')
        private_key = data.get('private_key')
        nonce = data.get('nonce')
        balance = data.get('balance')
        stake = data.get('stake')
        return cls(public_key, private_key, nonce, balance, stake)

    def __str__(self) -> str:
        return str(self.__class__) + ": " + str(self.__dict__)

    def set_stake(self, stake_amount: float) -> None:
        self.stake = stake_amount

    def get_private_key(self) -> str:
        if self.private_key is None:
            raise ValueError("Private key is not set, wallet is public!")
        return self.private_key

    def pending_balance_check(self, amount: float):
        return self.pending_balance - self.stake >= amount

    def stake_check(self, stake_amount: float):
        return self.pending_balance >= stake_amount

    def to_dict(self) -> dict:
        return {
            'public_key': self.public_key,
            'private_key': self.private_key,
            'nonce': self.nonce,
            'balance': self.balance,
            'stake': self.stake
        }
