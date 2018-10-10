import subprocess, time
from user_agent import generate_user_agent as user_agent
from threading import Timer
import config as cfg

class Extract:

    def __init__(self):
        self.start_time = time.time()
        self.max_requests_per_token = 200 #200
        self.minutes = int(self.max_requests_per_token * 2 * len(cfg.tokens) / 30) + 1
        self.urls = {
            'blockcypher_txs': 'https://api.blockcypher.com/v1/eth/main/txs',
            'ethergasstation': 'https://ethgasstation.info/json/ethgasAPI.json',
            'etherchain': 'https://www.etherchain.org/api/gasPriceOracle',
            'network_stats': 'https://api.ethpool.org/networkStats',
            'pool_stats': 'https://api.ethpool.org/poolStats',
            'block_cypher_pool_stats': 'https://api.blockcypher.com/v1/eth/main'
        }

    def _get_file_name(self, url):
        return 'output/' + str(int(time.time())) + '_' + url + '.json'

    def _get_subprocess_args(self, url):
        return ['wget', self._get_url(url), '-O', self._get_file_name(url)]

    def _get_url(self, url):
        if url == 'blockcypher_txs':
            return self.urls[url] + '?token=' + self.token
        return self.urls[url]

    def _download_every_second(self, token):
        self.token = token
        subprocess.call(self._get_subprocess_args('blockcypher_txs'))

    def _download_every_minute(self, url):
        subprocess.call(self._get_subprocess_args(url))

    def download_every_second(self):
        interval = 0
        for token in cfg.tokens:
            for i in range(1, self.max_requests_per_token + 1):
                Timer(interval, self._download_every_second, [token]).start()
                interval = interval + 2

    def download_every_minute(self):
        for i in range(self.minutes):
            for url in self.urls:
                if url == 'blockcypher_txs':
                    continue
                Timer(i * 15.0, self._download_every_minute, [url]).start()

if __name__ == '__main__':
    extract = Extract()
    extract.download_every_second()
    extract.download_every_minute()
