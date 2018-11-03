from metadata_db import Block, Transaction
from extract_block import Extract_block
from utility import get_session_db

class Load_block:

    def __init__(self):
        self.session = get_session_db()

    def _load_block(self, args):
        if not self.session.query(Block).filter_by(height = args['height']).first():
            print('# Loading block height in block table', args['height'], '\n')
            self.session.merge(Block(**args))
            self.session.commit()

    def _load_txGasUsed(self, args):
        tx = self.session.query(Transaction).filter_by(hash = args['hash']).first()
        tx.bck_id = args['block_height']
        tx.gas_used = args['gas_used']
        self.session.commit()

    def load_block_and_txGasUsed(self):
        extract = Extract_block()
        hashes = extract.get_hashes_without_block_id()
        for hash in hashes:
            bckId_gasUsed = extract.get_gasUsed(hash)
            if bckId_gasUsed:
                bck_id = bckId_gasUsed['block_height']
                print('\n\n# Loading tx gas used: ', hash, '\n', bckId_gasUsed)
                self._load_txGasUsed(bckId_gasUsed)
                if not extract.is_block_in_blockTbl(bck_id):
                    self._load_block(extract.get_block(bck_id))

if __name__ == '__main__':
    load = Load_block()
    load.load_block_and_txGasUsed()
