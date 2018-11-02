#utility.py
from random import randint
from inspect import Parameter, Signature
import config as cfg
import json, glob, time, subprocess, re
import dateutil.parser

class StructMeta(type):
    def __new__(cls, name, bases, dict):
        clsobj = super().__new__(cls, name, bases, dict)
        sig = cls.make_signature(clsobj.__fields__)
        setattr(clsobj, '__signature__', sig)
        return clsobj

    def make_signature(names):
        return Signature(
            Parameter(v, Parameter.POSITIONAL_OR_KEYWORD) for v in names
        )

class Structure(metaclass = StructMeta):
    __fields__ = []
    def __init__(self, *args, **kwargs):
        bond = self.__signature__.bind(*args, **kwargs)
        for name, val in bond.arguments.items():
            setattr(self, name, val)

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

def get_json_from_file(file_name):
    with open(file_name) as file:
        try:
            return json.load(file)
        except:
            return False

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
