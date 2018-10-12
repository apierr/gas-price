from metadata_db import Transaction, MemoryPool
from open_tx import Open_tx
from extract_block import Extract_block
from session_db import get_session_db
from sqlalchemy import text

class Load:

    def __init__(self):
        self.session = get_session_db()

    def _persist_to_db(self, row):
        self.session.merge(row)
        self.session.commit()

    def load_txs(self, rows):
        for row in rows:
            if not self.session.query(Transaction).filter_by(hash = row[0]).first():
                self._persist_to_db(Transaction(*row))

    def load_memory_pool(self, rows):
        for row in rows:
            if not self.session.query(MemoryPool).filter_by(height = row[0]).first():
                self._persist_to_db(MemoryPool(*row))

if __name__ == '__main__':
    load = Load()
    open_tx = Open_tx()
    load.load_txs(open_tx.get_txs())
    load.load_memory_pool(open_tx.get_memory_pool())
