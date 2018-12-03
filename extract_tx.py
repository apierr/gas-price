from threading import Timer
from utility import get_url, download_file, get_file_name

class Extract:

    def __init__(self):
        pass

    def _download(self, url_key):
        download_file(get_url(url_key), get_file_name(url_key))

    def download_tx(self):
        number_of_times_each_minute = 30
        interval = 60 / (number_of_times_each_minute)
        for i in range(number_of_times_each_minute):
            for url_key in ['pending_txs']:
                Timer(i * interval, self._download, [url_key]).start()

    def download_stats(self):
        number_of_times_each_minute = 4
        interval = 60 / (number_of_times_each_minute)
        for i in range(number_of_times_each_minute):
            for url_key in ['ether_gas_stn', 'ether_chain', 'net_stats', 'pools_stats', 'pool_stats', 'predictTable']:
                Timer(i * interval, self._download, [url_key]).start()

if __name__ == '__main__':
    extract = Extract()
    #extract.download_tx()
    extract.download_stats()
