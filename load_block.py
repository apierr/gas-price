from metadata_db import Transaction
from extract_block import Extract_block
from session_db import get_session_db

class Load_block:

    def __init__(self):
        self.session = get_session_db()

    def _load_bckId_gasUsed_into_tx(self, args):
        tx = self.session.query(Transaction).filter_by(tx_hash = args['hash']).first()
        print(hash)
        tx.bck_id = args['block_height']
        tx.tx_gas_used = args['gas_used']
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

if __name__ == '__main__':
    load = Load_block()
    load.load_bckId_gasUsed_into_txs()
