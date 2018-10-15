from metadata_db import Block, Transaction
from extract_block import Extract_block
from session_db import get_session_db
from open_block import Open_block

class Load_block:

    def __init__(self):
        self.session = get_session_db()

    def _load_bckId_gasUsed_into_tx(self, args):
        tx = self.session.query(Transaction).filter_by(hash = args['hash']).first()
        print(hash)
        tx.bck_id = args['block_height']
        tx.gas_used = args['gas_used']
        self.session.commit()

    def load_bckId_gasUsed_into_txs(self):
        extract_block = Extract_block()
        hashes = extract_block.get_hashes_without_block_id()
        for hash in hashes:
            print(hash)
            bckId_gasUsed = extract_block.get_bckId_gasUsed(hash)
            if bckId_gasUsed:
                print('bckId_gasUsed: ', bckId_gasUsed)
                self._load_bckId_gasUsed_into_tx(bckId_gasUsed)

    def _load_block(self, args):
        if not self.session.query(Block).filter_by(bck_id = args[0]).first():
            print(args[0])
            bck = Block(*args)
            self.session.merge(bck)
            self.session.commit()

    def load_blocks(self, bcks):
        for bck in bcks: self._load_block(bck)


if __name__ == '__main__':
    load = Load_block()
    load.load_bckId_gasUsed_into_txs()
    # open_block = Open_block()
    # load.load_blocks(open_block.get_blocks())
