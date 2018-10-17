import metadata_db as meta_db
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

    def get_txs(self):
        txs = []
        cls_attributes = self._get_cls_attributes(meta_db.Transaction)
        for file in get_files(self.pattern + '*pending_txs.json'):
            txs_json = get_json_from_file(file)
            if txs_json:
                for tx in txs_json:
                    tx['file_timestamp'] = get_timestamp_from_file(file)
                    txs.append(self._get_dict(tx, cls_attributes))
        return txs

    def get_net_stats(self):
        rows = []
        cls_attributes = self._get_cls_attributes(meta_db.NetworkStats)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_net_stats.json'):
            json = get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data']:
                json['data']['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_dict(json['data'], cls_attributes))
        return rows

    def get_pools_stats(self):
        rows = []
        cls_attributes = self._get_cls_attributes(meta_db.PoolsStats)
        print(cls_attributes)
        for file in get_files(self.pattern + '*_pools_stats.json'):
            json = get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data'] and json['data']['poolStats']:
                json = json['data']['poolStats']
                json['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_dict(json, cls_attributes))
        return rows

    def get_pending_txs_found(self):
        return self._get_rows(meta_db.PendingTransactionFound, '*_pending_txs_found.json')

    def get_ether_gas_stn(self):
        return self._get_rows(meta_db.EtherGasStation, '*_ether_gas_stn.json')

    def get_memory_pool(self):
        return self._get_rows(meta_db.MemoryPool, '*_pool_stats.json')

    def get_gas_oracle_ethchain(self):
        return self._get_rows(meta_db.GasOracleEthChain, '*_ether_chain.json')

    def _get_rows(self, table, file_extension):
        rows = []
        cls_attributes = self._get_cls_attributes(table)
        for file in get_files(self.pattern + file_extension):
            json = get_json_from_file(file)
            if json:
                json['file_timestamp'] = get_timestamp_from_file(file)
                rows.append(self._get_dict(json, cls_attributes))
        return rows

if __name__ == '__main__':
    open = Open_tx()
    print(open.get_txs())
    #print(open.get_memory_pool())
    # print(len(open.get_gas_oracle_ethchain()))
    # print(len(open.get_net_stats()))
    # print(len(open.get_pools_stats()))
    # print(open.get_ether_gas_stn())
    #print(open.get_pending_txs_found())
