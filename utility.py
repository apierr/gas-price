#utility.py
from random import randint
from sqlalchemy import create_engine
from metadata_db import Base
from sqlalchemy.orm import sessionmaker
import config as cfg
import json, glob, time, subprocess, re
import dateutil.parser, shutil

urls = {
    'transaction': 'https://api.blockcypher.com/v1/eth/main/txs/',
    'block': 'https://api.blockcypher.com/v1/eth/main/blocks/',
    'pending_txs': 'https://api.blockcypher.com/v1/eth/main/txs',
    'ether_gas_stn': 'https://ethgasstation.info/json/ethgasAPI.json',
    'ether_gas_price_wait_stn': 'https://ethgasstation.info/json/priceWait.json',
    'ether_chain': 'https://www.etherchain.org/api/gasPriceOracle',
    'net_stats': 'https://api.ethpool.org/networkStats',
    'pools_stats': 'https://api.ethpool.org/poolStats',
    'pool_stats': 'https://api.blockcypher.com/v1/eth/main'
}

def _get_random_ip():
    return '.'.join([str(randint(0, 255)) for x in range(4)])

def _get_random_token():
    return '?token=' + cfg.tokens[randint(0, len(cfg.tokens) - 1)]

def get_file_name(url_key, arg = ''):
    return cfg.output_path + str(int(time.time())) + '_' + arg + '_' + url_key + '.json'

def get_session_db():
    engine = get_engine()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    return DBSession()

def get_engine():
    return create_engine(cfg.db_url)

def get_timestamp_from_file(file_name):
    return re.search('/(\d{10})_', file_name).group(1)

def get_json_from_csv_file(file_name, fieldnames = ('ts', 'pending_txs_found')):
    import csv
    json = []
    csvfile = open(file_name, 'r')
    reader = csv.DictReader( csvfile, fieldnames)
    for row in reader:
        json.append(dict(row))
    return json

def get_json_from_file(file_name, is2move = False):
    with open(file_name) as file:
        try:
            result = json.load(file)
        except:
            result = False
    if is2move: shutil.move(file_name, cfg.dst_files_read)
    return result

def get_cls_attributes(cls):
    return cls.__fields__

def download_file(url, file_name):
    subprocess.call(['curl', url, '-H', _get_random_ip() ,'-o', file_name])

def get_files(pattern):
    return glob.glob(pattern)

def get_url(url_key, arg = ''):
    return urls[url_key] + arg + _get_random_token()

## TODO it gives different timestamp based on system CEST vs UTC
def get_unix_ts(date):
    dt = dateutil.parser.parse(date)
    return int(time.mktime(dt.timetuple()))
