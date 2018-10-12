import metadata_db
from utility import get_json_from_file, get_files
import config as cfg

class Open_tx:

    def __init__(self):
        self.pattern = cfg.output_path

    def _get_cls_attributes(self, cls):
        return [i for i in cls.__dict__.keys() if i[:1] != '_']

    def _get_list(self, json, attributes):
        return list(filter(None.__ne__, [json.get(i, None) for i in attributes]))

    def get_memory_pool(self):
        pool_stats = []
        cls_attributes = self._get_cls_attributes(metadata_db.MemoryPool)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_pool_stats.json'):
            json = get_json_from_file(file)
            if json:
                pool_stats.append(self._get_list(json, cls_attributes))
        return pool_stats

    def get_txs(self):
        txs = []
        cls_attributes = self._get_cls_attributes(metadata_db.Transaction)
        print('cls_attributes: ', cls_attributes)
        for file in get_files(self.pattern + '*_txs.json'):
            txs_json = get_json_from_file(file)
            if txs_json:
                for tx in txs_json:
                    txs.append(self._get_list(tx, cls_attributes))
        return txs

if __name__ == '__main__':
    open_tx = Open_tx()
    print(len(open_tx.get_txs()))
    print(open_tx.get_memory_pool())
