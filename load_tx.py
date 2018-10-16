from metadata_db import Transaction, MemoryPool, GasOracleEthChain, NetworkStats, \
PoolsStats, PendingTransactionFound, EtherGasStation
from open_tx import Open_tx
from extract_block import Extract_block
from session_db import get_session_db
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

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
            if not self.session.query(MemoryPool).filter_by(file_timestamp = row[0]).first():
                self._persist_to_db(MemoryPool(*row))

    def load_gas_oracle_ethchain(self, rows):
        for row in rows:
            if not self.session.query(GasOracleEthChain).filter_by(file_timestamp = row[0]).first():
                self._persist_to_db(GasOracleEthChain(*row))

    def load_net_stats(self, rows):
        for row in rows:
            if not self.session.query(NetworkStats).filter_by(file_timestamp = row[0]).first():
                self._persist_to_db(NetworkStats(*row))

    def load_pools_stats(self, rows):
        for row in rows:
            if not self.session.query(PoolsStats).filter_by(file_timestamp = row[0]).first():
                self._persist_to_db(PoolsStats(*row))

    def load_pending_txs_found(self, rows):
        for row in rows[1:]:
            if not self.session.query(PendingTransactionFound).filter_by(ts = row[0]).first():
                self._persist_to_db(PendingTransactionFound(*row))

    def load_ether_gas_stn(self, rows):
        for row in rows:
            try:
                self.session.query(EtherGasStation).filter_by(file_timestamp = row[0]).one()
            except NoResultFound:
                self._persist_to_db(EtherGasStation(*row))

if __name__ == '__main__':
    load = Load()
    open = Open_tx()
    # load.load_txs(open.get_txs())
    # load.load_memory_pool(open.get_memory_pool())
    # load.load_gas_oracle_ethchain(open.get_gas_oracle_ethchain())
    load.load_net_stats(open.get_net_stats())
    # load.load_pools_stats(open.get_pools_stats())
    # load.load_ether_gas_stn(open.get_ether_gas_stn())
    #load.load_pending_txs_found(open.get_pending_txs_found())
