import metadata_db
from utility import get_json_from_file, get_files, get_timestamp_from_file, get_json_from_csv_file
import config as cfg

class Open_tx:

    def __init__(self):
        self.pattern = cfg.output_path

    def _get_cls_attributes(self, cls):
        return [i for i in cls.__dict__.keys() if i[:1] != '_']

    def _get_list(self, json, attributes):
        return list(filter(None.__ne__, [json.get(i, None) for i in attributes]))

    def _get_dict(self, json, attributes):
        return {i : json.get(i, None) for i in attributes}

    def get_memory_pool(self):
        pool_stats = []
        cls_attributes = self._get_cls_attributes(metadata_db.MemoryPool)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_pool_stats.json'):
            json = get_json_from_file(file)
            if json:
                json['file_timestamp'] = get_timestamp_from_file(file)
                pool_stats.append(self._get_list(json, cls_attributes))
        return pool_stats

    def get_txs(self):
        txs = []
        cls_attributes = self._get_cls_attributes(metadata_db.Transaction)
        for file in get_files(self.pattern + '*_txs.json'):
            txs_json = get_json_from_file(file)
            if txs_json:
                for tx in txs_json:
                    txs.append(self._get_list(tx, cls_attributes))
        return txs

    def get_gas_oracle_ethchain(self):
        rows = []
        cls_attributes = self._get_cls_attributes(metadata_db.GasOracleEthChain)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_ether_chain.json'):
            json = get_json_from_file(file)
            if json:
                json['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_list(json, cls_attributes))
        return rows

    def get_net_stats(self):
        rows = []
        cls_attributes = self._get_cls_attributes(metadata_db.NetworkStats)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_net_stats.json'):
            json = get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data']:
                json['data']['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_dict(json['data'], cls_attributes))
        return rows

    def get_pools_stats(self):
        rows = []
        cls_attributes = self._get_cls_attributes(metadata_db.PoolsStats)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_pools_stats.json'):
            json = get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data'] and json['data']['poolStats']:
                json = json['data']['poolStats']
                json['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_list(json, cls_attributes))
        return rows

    def get_pending_txs_found(self):
        rows = []
        cls_attributes = self._get_cls_attributes(metadata_db.PendingTransactionFound)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_pending_txs_found.csv'):
            jsons = get_json_from_csv_file(file)
            for json in jsons:
                rows.append(self._get_list(json, cls_attributes))
        return rows

    def get_ether_gas_stn(self):
        rows = []
        cls_attributes = self._get_cls_attributes(metadata_db.EtherGasStation)
        for file in get_files(self.pattern + '*_ether_gas_stn.json'):
            json = get_json_from_file(file)
            if json:
                json['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_list(json, cls_attributes))
        return rows

if __name__ == '__main__':
    open = Open_tx()
    # print(len(open.get_txs()))
    # print(open.get_memory_pool())
    # print(open.get_gas_oracle_ethchain())
    print(len(open.get_net_stats()))
    # print(open.get_pools_stats())
    # print(open.get_ether_gas_stn())
    #print(open.get_pending_txs_found())
