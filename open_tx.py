import metadata_db as meta_db
import utility as util
import config as cfg

class Open_tx:

    def __init__(self):
        self.pattern = cfg.output_path

    def _get_dict(self, json, attributes):
        return {i : json.get(i, None) for i in attributes}
    def _get_list(self, json, attributes):
        return list(filter(None.__ne__, [json.get(i, None) for i in attributes]))

    def _get_rows(self, table, file_extension):
        rows = []
        cls_attributes = util.get_cls_attributes(table)
        print(cls_attributes)
        for file in util.get_files(self.pattern + file_extension):
            json = util.get_json_from_file(file)
            if json:
                json['file_timestamp'] = util.get_timestamp_from_file(file)
                rows.append(self._get_dict(json, cls_attributes))
        return rows

    def get_tx(self):
        txs = []
        cls_attributes = util.get_cls_attributes(meta_db.Transaction)
        for file in util.get_files(self.pattern + '*pending_txs.json'):
            txs_json = util.get_json_from_file(file)
            if txs_json:
                for tx in txs_json:
                    tx['file_timestamp'] = util.get_timestamp_from_file(file)
                    txs.append(self._get_dict(tx, cls_attributes))
        return txs

    def get_netStats(self):
        rows = []
        cls_attributes = util.get_cls_attributes(meta_db.NetStats)
        for file in util.get_files(self.pattern + '*_net_stats.json'):
            json = util.get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data']:
                json['data']['file_timestamp'] = util.get_timestamp_from_file(file)
                rows.append(self._get_dict(json['data'], cls_attributes))
        return rows

    def get_poolsStats(self):
        rows = []
        cls_attributes = util.get_cls_attributes(meta_db.PoolsStats)
        for file in util.get_files(self.pattern + '*_pools_stats.json'):
            json = util.get_json_from_file(file)
            if json and json['status'] == 'OK' and json['data'] and json['data']['poolStats']:
                json = json['data']['poolStats']
                json['file_timestamp'] = util.get_timestamp_from_file(file)
                rows.append(self._get_dict(json, cls_attributes))
        return rows

    def get_pending_txs_found(self):
        return self._get_rows(meta_db.PendingTransactionFound, '*_pending_txs_found.json')

    def get_etherGasStation(self):
        return self._get_rows(meta_db.EtherGasStation, '*_ether_gas_stn.json')

    def get_memoryPool(self):
        return self._get_rows(meta_db.MemoryPool, '*_pool_stats.json')

    def get_oracleEthchain(self):
        return self._get_rows(meta_db.OracleEthChain, '*_ether_chain.json')

if __name__ == '__main__':
    open = Open_tx()
    # print(len(open.get_tx()))
    # print(len(open.get_memoryPool()))
    # print(len(open.get_oracleEthchain()))
    # print(len(open.get_netStats()))
    print(open.get_poolsStats())
    # print(open.get_etherGasStation())
    #print(len(open.get_pending_txs_found()))
