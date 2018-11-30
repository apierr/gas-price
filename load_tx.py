from metadata_db import Transaction, MemoryPool, OracleEthChain, NetStats, \
PoolsStats, EtherGasStation
from open_tx import Open_tx
from extract_block import Extract_block
from utility import get_session_db
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

class Load:

    def __init__(self):
        self.session = get_session_db()

    def _persist_to_db(self, tableObj):
        self.session.merge(tableObj)
        self.session.commit()

    def _persist_rows_to_db(self, rows, table):
        for row in rows:
            try:
                self.session.query(table).filter_by(file_timestamp = row['file_timestamp']).one()
            except NoResultFound:
                self._persist_to_db(table(**row))

    def load_tx(self, rows):
        for row in rows:
            if not self.session.query(Transaction).filter_by(hash = row['hash']).first():
                self._persist_to_db(Transaction(**row))

    # def load_pending_txs_found(self, rows):
    #     for row in rows[1:]:
    #         if not self.session.query(PendingTransactionFound).filter_by(ts = row[0]).first():
    #             self._persist_to_db(PendingTransactionFound(*row))

    def load_memoryPool(self, rows):
        self._persist_rows_to_db(rows, MemoryPool)

    def load_poolsStats(self, rows):
        self._persist_rows_to_db(rows, PoolsStats)

    def load_etherGasStation(self, rows):
        self._persist_rows_to_db(rows, EtherGasStation)

    def load_oracleEthchain(self, rows):
        self._persist_rows_to_db(rows, OracleEthChain)

    def load_netStats(self, rows):
        self._persist_rows_to_db(rows, NetStats)

if __name__ == '__main__':
    load = Load()
    open = Open_tx(is2move = True)
    # load.load_tx(open.get_tx())
    load.load_memoryPool(open.get_memoryPool())
    load.load_oracleEthchain(open.get_oracleEthchain())
    load.load_netStats(open.get_netStats())
    load.load_poolsStats(open.get_poolsStats())
    load.load_etherGasStation(open.get_etherGasStation())
    # load.load_pending_txs_found(open.get_pending_txs_found())
