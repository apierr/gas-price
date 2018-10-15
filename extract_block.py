import urllib.request, json, time
from random import randint
from session_db import get_session_db
import config as cfg
from metadata_db import Transaction, Block
import subprocess
from utility import get_url, download_file, get_file_name, get_url

class Extract_block:

    def __init__(self):
        self.bckId_gasUsed_keys = ['hash', 'block_height', 'gas_used']

    def _get_json(self, hash):
        print(get_url('transaction', hash))
        try:
            with urllib.request.urlopen(get_url('transaction', hash)) as url:
                return json.loads(url.read().decode())
        except:
            default_values = [hash, 0, None]
            return dict(zip(self.bckId_gasUsed_keys, default_values))


    def _get_subprocess_args(self, arg):
        return ['wget', get_url('block', arg), '-O', self._get_file_name('block')]

    def _get_txsBckId_notIn_blockTable(self):
        subquery = get_session_db().query(Block.bck_id)
        query = get_session_db().query(Transaction.bck_id) \
            .filter(Transaction.bck_id > 0) \
            .filter(Transaction.bck_id.notin_(subquery)).distinct().all()
        return [ str(col[0]) for col in query]

    def download_block(self):
        url_key = 'block'
        for bck_id in self._get_txsBckId_notIn_blockTable():
            print(get_url(url_key, bck_id), get_file_name(url_key, bck_id))
            # download_file(get_url(url_key, bck_id), get_file_name(url_key, bck_id))

    def get_bckId_gasUsed(self, hash):
        json = self._get_json(hash)
        return {key: json.get(key) for key in self.bckId_gasUsed_keys}

    def get_hashes_without_block_id(self):
        return [ col[0] for col in get_session_db().query(Transaction.hash) \
            .filter(Transaction.bck_id.is_(None)).all() ]


if __name__ == '__main__':
    extract = Extract_block()
    hashes = extract.get_hashes_without_block_id()
    print(len(hashes))
    for hash in hashes[-1:]:
        print(extract.get_bckId_gasUsed(hash))
        extract.download_block()
