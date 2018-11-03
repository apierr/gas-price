import urllib.request, json, time
from random import randint
from utility import get_session_db
import config as cfg
from metadata_db import Transaction, Block
import utility as util

class Extract_block:

    def __init__(self):
        self.tx_args = ['hash', 'block_height', 'gas_used']
        self.block_args = ['height', 'time', 'hash', 'prev_block', 'size', 'fees', 'total', 'n_tx']

    def _get_json(self, hash):
        print(util.get_url('transaction', hash))
        try:
            with urllib.request.urlopen(util.get_url('transaction', hash)) as url:
                return json.loads(url.read().decode())
        except:
            default_values = [hash, 0, None]
            return dict(zip(self.tx_args, default_values))

    def _get_json_block(self, bck_id):
        print('block_height: ', bck_id, '\n', util.get_url('block', bck_id))
        try:
            with urllib.request.urlopen(util.get_url('block', bck_id)) as url:
                return json.loads(url.read().decode())
        except:
            print('#####Error in extractin block', bck_id, util.get_url('block', bck_id))

    def is_block_in_blockTbl(self, bckId):
        return get_session_db().query(Block.height)\
            .filter(Block.height == bckId).first()

    def get_gasUsed(self, hash):
        json = self._get_json(hash)
        return {key: json.get(key) for key in self.tx_args}

    def get_block(self, bkc_id):
        json = self._get_json_block(str(bkc_id))
        return {key: json.get(key) for key in util.get_cls_attributes(Block)}

    def get_hashes_without_block_id(self):
        return [ col[0] for col in get_session_db().query(Transaction.hash) \
            .filter(Transaction.bck_id.is_(None)).all() ]

if __name__ == '__main__':
    extract = Extract_block()
    # hashes = extract.get_hashes_without_block_id()
    print(extract.get_block(6507223))
