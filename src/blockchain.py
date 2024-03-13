from block import Block


class Blockchain:

    def __init__(self):
        self.blocks : list[Block] = list()
        self.validators : dict[str,int] = dict()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_block(self, block):
        self.blocks.append(block)

    def validate_chain(self):
        pass

    def set_validator(self, address : str, stake : int):
        self.validators[address] = stake

    def last_block(self) -> Block:
        return self.blocks[-1]
    
    def balance_check():
        pass