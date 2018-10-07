from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Transaction (Base):
    __tablename__ = 'transaction'
    tx_id = Column(Integer, primary_key = True)
    tx_hash = Column(String(64), unique = True)
    tx_ts = Column(Integer, nullable = False)
    tx_gas_limit = Column(Integer, nullable = True)
    gas_price = Column(Numeric, nullable = True)
    block_id = Column(Integer, ForeignKey('block.block_id'), nullable = True)

class Block (Base):
    __tablename__ = 'block'
    block_id = Column(Integer, primary_key = True)
    block_hash = Column(String(64), unique = True)
    block_ts = Column(Integer, nullable = False)
    block_gas_limit = Column(Integer, nullable = True)
    block_time = Column(Integer, nullable = False)
    reward = Column(Numeric, nullable = True)
    fees = Column(Numeric, nullable = True)

class EtherGasStation (Base):
    # https://ethgasstation.info/json/ethgasAPI.json
    __tablename__ = 'ethergasstation'
    egs_id = Column(Integer, primary_key = True)
    egs_ts = Column(Integer, nullable = False)
    average = Column(Numeric, nullable = True)
    fastestWait = Column(Numeric, nullable = True)
    fastWait = Column(Numeric, nullable = True)
    egs_fast = Column(Numeric, nullable = True)
    safeLowWait = Column(Numeric, nullable = True)
    blockNum = Column(Numeric, nullable = True)
    avgWait = Column(Numeric, nullable = True)
    block_time = Column(Numeric, nullable = True)
    speed = Column(Numeric, nullable = True)
    egs_fastest = Column(Numeric, nullable = True)
    egs_safeLow = Column(Numeric, nullable = True)

class EtherChain (Base):
    # https://www.etherchain.org/api/gasPriceOracle
    # https://www.etherchain.org/tools/gasPriceOracle
    __tablename__ = 'etherchain'
    ec_id = Column(Integer, primary_key = True)
    ec_ts = Column(Integer, nullable = False)
    ec_safeLow = Column(Numeric, nullable = True)
    standard = Column(Numeric, nullable = True)
    ec_fast = Column(Numeric, nullable = True)
    ec_fastest = Column(Numeric, nullable = True)

if __name__ == '__main__':
    engine = create_engine('sqlite:///tx.db')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
