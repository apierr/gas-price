import urllib.request, json
from random import randint
from session_db import get_session_db
import config as cfg
from metadata_db import Transaction

class Extract_block:

    def __init__(self):
        self.urls = {
            'transaction': 'https://api.blockcypher.com/v1/eth/main/txs/',
            'block': 'https://api.blockcypher.com/v1/eth/main/blocks/'
        }
        self.bckId_gasUsed_keys = ['hash', 'block_height', 'gas_used']

    def _get_json(self, hash):
        print(self._get_url(hash))
        try:
            with urllib.request.urlopen(self._get_url(hash)) as url:
                print(self._get_url(hash))
                return json.loads(url.read().decode())
        except:
            default_values = [hash, 0, None]
            return dict(zip(self.bckId_gasUsed_keys, default_values))

    def _get_url(self, hash):
        return self.urls['transaction'] + hash + '?token=' + cfg.tokens[randint(0,14)]

    def get_bckId_gasUsed(self, hash):
        json = self._get_json(hash)
        print('###################', json)
        return {key: json.get(key) for key in self.bckId_gasUsed_keys}

    def get_hashes_without_block_id(self):
        return [ col[0] for col in get_session_db().query(Transaction.tx_hash) \
            .filter(Transaction.bck_id.is_(None)).all() ]

if __name__ == '__main__':
    extract_block = Extract_block()
    hashes = extract_block.get_hashes_without_block_id()
    for hash in hashes[-1:]:
        print(extract_block.get_bckId_gasUsed(hash))
