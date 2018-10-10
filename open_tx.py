import metadata_db
from utility import get_json_from_file, get_files

class Open_tx:

    def __init__(self):
        self.pattern = './output/*_txs.json'

    def _get_class_attributes(self, cls):
        return [i[3:] for i in cls.__dict__.keys() if i[:1] != '_'][1:-2]

    def _get_files(self):
        return glob.glob(self.pattern)

    def get_txs(self):
        txs = []
        cls_attributes = self._get_class_attributes(metadata_db.Transaction)
        for file in get_files(self.pattern):
            txs_json = get_json_from_file(file)
            if txs_json:
                for tx in txs_json:
                    print(tx['hash'])
                    txs.append([tx[i] for i in  cls_attributes])
        return txs

if __name__ == '__main__':
    open_tx = Open_tx()
    open_tx.get_txs()
