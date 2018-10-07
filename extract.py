import wget, time

class Extract:

    def __init__(self):
        self.start_time = time.time()
        self.max_requests_per_token = 2 #200
        self.tokens = [
            '8f8751bd9aa7419fb9ca04c72b47002f',
            'ca1af79ec91947c0845a4c1e0794a568',
            '74991f4042ae47f689deb587b8d3ed54',
            'a3ff4595a44e4c21a4ae621cfc58d376'
        ]
        self.url = 'https://api.blockcypher.com/v1/eth/main/txs'

    def _get_file_name(self, i):
        return str(i) + '_' + self.token[0:2] +'_txs.json'

    def _get_url(self):
        return self.url + '?token=' + self.token

    def _download_tx(self, i):
        wget.download(url = self._get_url(), out = self._get_file_name(i))
        time.sleep(2.0 - ((time.time() - self.start_time) % 2.0))

    def download_txs(self):
        for self.token in self.tokens:
            for i in range(self.max_requests_per_token): self._download_tx(i)

if __name__ == '__main__':
    extract = Extract()
    txs.download_txs()
