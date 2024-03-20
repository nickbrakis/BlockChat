from Crypto.PublicKey import RSA

class Wallet:

    def __init__(self):
        self.nonce = 0
        self.balance = 0
        self.stake = 0

    def __str__(self):
        """Returns a string representation of a Wallet object."""
        return str(self.__class__) + ": " + str(self.__dict__)

    def get_balance(self):
        pass

    def stake(self, amount):
        pass

    def get_address(self):
        return self.public_key

class PrivateWallet(Wallet) :
    def __init__(self):
        # Generate a private key of key length of 1024 bits.
        key = RSA.generate(1024)
        self.private_key = key.exportKey().decode('ISO-8859-1')
        # Generate the public key from the above private key.
        self.public_key = key.publickey().exportKey().decode('ISO-8859-1')
    
    def get_private_key(self):
        return self.private_key


class PublicWallet(Wallet) :
    def __init__(self, public_key : str):
        self.public_key = public_key

