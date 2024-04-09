# pylint: disable=missing-docstring
from block import Block
from pydantic import BaseModel


class Blockchain(BaseModel):
    blocks: list[Block] = list()

    def __init__(self, blocks: list[Block] = list()):
        super().__init__()
        self.blocks: list[Block] = blocks

    @classmethod
    def from_dict(cls, data: dict):
        blocks = []
        for block_dict in data.get('blocks'):
            blocks.append(Block.from_dict(block_dict))
        return cls(blocks)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def add_block(self, block):
        self.blocks.append(block)

    def validate_chain(self):
        if len(self.blocks) == 1:
            return True
        for i in range(1, len(self.blocks)):
            if self.blocks[i].validate_block(self) is False:
                return False
        return True

    def last_block(self) -> Block:
        return self.blocks[-1]
