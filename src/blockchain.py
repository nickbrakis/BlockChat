from block import Block

class Blockchain:
    def __init__(self):
        self.blocks : list[Block] = list()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_block(self, block):
        self.blocks.append(block)

    def validate_chain(self):
        for i in range(1, len(self.blocks)):
            if self.blocks[i].validate_block(self) == False:
                return False
        return True

    def last_block(self) -> Block:
        return self.blocks[-1]
    

