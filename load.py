from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from metadata_db import Base, Transaction
from extract_from_file import Extract_from_file

class Load:

    def __init__(self, db_name = 'tx.db'):
        self.db_name = db_name
        self._set_session()

    def _set_session(self):
        engine = create_engine('///'.join(['sqlite:', self.db_name]))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind = engine)
        self.session = DBSession()

    def load_tx(self, args):
        if not self.session.query(Transaction).filter_by(tx_hash = args[1]).first():
            tx = Transaction(*args)
            self.session.merge(tx)
            self.session.commit()

    def get_hashes_without_block_id(self):
        return [ col[0] for col in self.session.query(Transaction.tx_hash) \
            .filter(Transaction.bck_id.is_(None)).all() ]

    def load_txs(self, txs):
        for tx in txs: self.load_tx(tx)

if __name__ == '__main__':
    load = Load('tx.db')
    extract = Extract_from_file()
    load.load_txs(extract.get_txs())
