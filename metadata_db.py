from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, create_engine
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utility import get_unix_ts, Structure
import re
import config as cfg
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from utility import StructMeta

Base = declarative_base()

class FinalMeta(DeclarativeMeta, StructMeta):
    print(type(Base), type(Structure))

class Transaction (Base, Structure, metaclass = FinalMeta):
    # https://api.blockcypher.com/v1/eth/main/txs (ok)
    __tablename__ = 'tx'
    __fields__ = ['hash', 'file_timestamp', 
    'received', 'gas_limit', 'gas_price', 'fees', 'double_spend']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer)
    hash = Column(String(64), unique = True)
    received = Column(Integer, nullable = False)
    gas_limit = Column(Integer, nullable = True)
    gas_price = Column(Numeric, nullable = True)
    fees = Column(BIGINT(unsigned=True), nullable = True)
    double_spend = Column(Boolean, nullable = True)
    gas_used = Column(Integer, nullable = True)
    bck_id = Column(Integer, ForeignKey('block.bck_id'), nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class Block (Base):
    # https://api.blockcypher.com/v1/eth/main/blocks/7
    # https://www.blockcypher.com/dev/ethereum/#block
    __tablename__ = 'block'
    bck_id = Column(Integer, primary_key = True)
    bck_time = Column(Integer, nullable = False)
    bck_hash = Column(String(64), nullable = False, unique = True)
    bcl_prev_block = Column(String(64), nullable = True, unique = True)
    bck_size = Column(Integer, nullable = True)
    bck_fees = Column(Integer, nullable = True)
    bkc_total = Column(Integer, nullable = True)
    bck_n_tx = Column(Integer, nullable = True)
    bck_reward = Column(Integer, nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, height, time, hash, prev_block, size, fees, total, n_tx):
        self.bck_id = height
        self.bck_time = get_unix_ts(time)
        self.bck_hash = hash
        self.bck_prev_block = prev_block
        self.bck_size = size
        self.bck_fees = fees
        self.bck_total = total
        self.bck_n_tx = n_tx

class NetStats (Base, Structure, metaclass = FinalMeta):
    # https://aqats
    __tablename__ = 'netStats'
    __fields__ = ['file_timestamp', 'time', 'blockTime', 'difficulty', 'hashrate', 'usd', 'btc']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, unique = True)
    time = Column(Integer, nullable = False)
    blockTime = Column(Numeric, nullable = False)
    difficulty = Column(Integer, nullable = False)
    hashrate = Column(Integer, nullable = False)
    usd = Column(Numeric, nullable = True)
    btc = Column(Numeric, nullable = True)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class PoolsStats (Base, Structure, metaclass = FinalMeta):
    # https://api.ethpool.org/poolStats
    # https://ethermine.org/api/pool#stats
    __tablename__ = 'poolsStats'
    __fields__ = ['file_timestamp', 'hashRate', 'miners', 'workers', 'blocksPerHour']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, nullable = False)
    hashRate = Column(Numeric, nullable = False)
    miners =  Column(Integer, nullable = False)
    workers = Column(Integer, nullable = False)
    blocksPerHour = Column(Numeric, nullable = False)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class MemoryPool(Base, Structure, metaclass = FinalMeta):
    # https://api.blockcypher.com/v1/eth/main
    # https://www.blockcypher.com/dev/ethereum/#blockchain
    __tablename__ = 'memoryPool'
    __fields__ = ['file_timestamp', 'height', 'time', 'unconfirmed_count', 'peer_count',
    'high_gas_price', 'medium_gas_price', 'low_gas_price', 'last_fork_height']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, unique = True)
    height = Column(Integer, nullable = False)
    time = Column(Integer, nullable = False)
    unconfirmed_count = Column(Integer, nullable = False)
    high_gas_price = Column(Integer, nullable = False)
    medium_gas_price = Column(Integer, nullable = False)
    low_gas_price = Column(Integer, nullable = False)
    last_fork_height = Column(Integer, nullable = False)
    peer_count = Column(Integer, nullable = False)

    # For passing position arguments to the creation of the Transaction object
    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class EtherGasStation (Base, Structure, metaclass = FinalMeta):
    # https://ethgasstation.info/json/ethgasAPI.json (ok)
    __tablename__ = 'etherGasStation'
    __fields__ = ['file_timestamp', 'average', 'fastestWait', 'fastWait', 'fast',
    'safeLowWait', 'blockNum', 'avgWait', 'block_time', 'speed', 'fastest', 'safeLow']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, unique = True)
    average = Column(Numeric, nullable = True)
    fastestWait = Column(Numeric, nullable = True)
    fastWait = Column(Numeric, nullable = True)
    fast = Column(Numeric, nullable = True)
    safeLowWait = Column(Numeric, nullable = True)
    blockNum = Column(Integer, nullable = True)
    avgWait = Column(Numeric, nullable = True)
    block_time = Column(Numeric, nullable = True)
    speed = Column(Numeric, nullable = True)
    fastest = Column(Numeric, nullable = True)
    safeLow = Column(Numeric, nullable = True)

    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class OracleEthChain(Base, Structure, metaclass = FinalMeta):
    # https://www.etherchain.org/api/gasPriceOracle (ok)
    # https://www.etherchain.org/tools/gasPriceOracle
    __tablename__ = 'oracleEthchain'
    __fields__ = ['file_timestamp', 'safeLow', 'standard', 'fast', 'fastest']
    id = Column(Integer, primary_key = True)
    file_timestamp = Column(Integer, nullable = False, unique = True)
    safeLow = Column(Numeric, nullable = True)
    standard = Column(Numeric, nullable = True)
    fast = Column(Numeric, nullable = True)
    fastest = Column(Numeric, nullable = True)

    def __init__(self, *args, **kwargs):
        Structure.__init__(self, *args, **kwargs)

class PendingTransactionFound(Base):
    # https://etherscan.io/txsPending
    __tablename__ = 'pendingtxsfound'
    id = Column(Integer, primary_key = True)
    ts = Column(Integer, nullable = False)
    pending_txs_found = Column(Integer, nullable = False)

    def __init__(self, ts, pending_txs_found):
        self.ts = get_unix_ts(ts) # '%m/%d/%Y %I:%M:%S %p'
        self.pending_txs_found = pending_txs_found

if __name__ == '__main__':
    engine = create_engine(cfg.db_url)
    Session = sessionmaker(bind = engine)
    Base.metadata.create_all(engine)
