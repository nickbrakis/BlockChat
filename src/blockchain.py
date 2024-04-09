# pylint: disable=missing-docstring
from block import Block
from pydantic import BaseModel


class Blockchain(BaseModel):
    blocks: list[Block] = list()

    def __init__(self, blocks: list[Block] = list()):
        super().__init__()
        self.blocks: list[Block] = blocks

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_block(self, block):
        self.blocks.append(block)

    def validate_chain(self):
        for i in range(1, len(self.blocks)):
            if self.blocks[i].validate_block(self) is False:
                return False
        return True

    def last_block(self) -> Block:
        return self.blocks[-1]

    def to_dict(self):
        return {
            'blocks': [block.to_dict() for block in self.blocks],
        }
