from metadata_db import Transaction
from open_tx import Open_tx
from extract_block import Extract_block
from session_db import get_session_db

class Load:

    def __init__(self):
        self.session = get_session_db()

    def _load_tx(self, args):
        if not self.session.query(Transaction).filter_by(tx_hash = args[1]).first():
            tx = Transaction(*args)
            print(args[1])
            self.session.merge(tx)
            self.session.commit()

    def load_txs(self, txs):
        for tx in txs: self._load_tx(tx)

if __name__ == '__main__':
    load = Load()
    open_tx = Open_tx()
    load.load_txs(open_tx.get_txs())
