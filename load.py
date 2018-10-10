from metadata_db import Transaction
from extract_from_file import Extract_from_file
from extract_block import Extract_block
from db_session import get_session_db

class Load:

    def __init__(self):
        self.session = get_session_db()

    def _load_tx(self, args):
        if not self.session.query(Transaction).filter_by(tx_hash = args[1]).first():
            tx = Transaction(*args)
            self.session.merge(tx)
            self.session.commit()

    def _load_bckId_gasUsed_into_tx(self, args):
        tx = self.session.query(Transaction).filter_by(tx_hash = args['hash']).first()
        print(hash)
        tx.bck_id = args['block_height']
        tx.tx_gas_used = args['gas_used']
        self.session.commit()

    def load_txs(self, txs):
        for tx in txs: self._load_tx(tx)

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
    load = Load()
    # extract = Extract_from_file()
    # load.load_txs(extract.get_txs())
    load.load_bckId_gasUsed_into_txs()
