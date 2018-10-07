import json

class Load:

    def __init__(self):
        self.x = ''

    def _load(self):
        with open('0_8f_txs.json', 'r') as f:
            txs = json.load(f)
        return txs

    def _parse(self):
        for tx in self._load():
            print(tx['hash'])

if __name__ == '__main__':
    load = Load()
    load._parse()
