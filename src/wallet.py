# pylint: disable=missing-docstring

class Wallet:
    '''Wallet class for the blockchain.'''

    def __init__(self, public_key: str,  private_key: str = -1, nonce: int = 0, balance: int = 0, stake: int = 0):
        self.private_key = private_key
        self.public_key = public_key
        self.nonce = nonce
        self.balance = balance
        self.stake = stake
        self.pending_balance = balance

    def __str__(self) -> str:
        """Returns a string representation of a Wallet object."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def set_stake(self, stake_amount: int) -> None:
        '''Sets the stake amount for the wallet.'''
        self.stake = stake_amount

    def get_private_key(self) -> str:
        '''Returns the private key for the wallet, if it exists. Otherwise, raises an error'''
        if self.private_key == -1:
            raise ValueError("Private key is not set, wallet is public!")
        return self.private_key

    def get_nonce(self):
        '''Returns the nonce for the wallet and auto-incements.'''
        while True:
            yield self.nonce
            self.nonce += 1

    def pending_balance_check(self, amount: int):
        '''Checks if the pending balance is greater than the transaction amount.'''
        return self.pending_balance - self.stake >= amount
