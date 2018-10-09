import glob, json
import metadata_db

class Extract_from_file:

    def __init__(self):
        self.pattern = './output/*_txs.json'

    def _get_class_attributes(self, cls):
        return [i[3:] for i in cls.__dict__.keys() if i[:1] != '_'][1:-1]

    def _get_data(self, json, cls_attributes):
        return [json[i] for i in  cls_attributes]

    def _get_files(self):
        return glob.glob(self.pattern)

    def _get_json(self, file_name):
        with open(file_name) as file: return json.load(file)

    def get_txs(self):
        txs = []
        cls_attributes = self._get_class_attributes(metadata_db.Transaction)
        for file in self._get_files():
            jsons = self._get_json(file)
            for json in jsons:
                txs.append(self._get_data(json, cls_attributes))
            break
        return txs

if __name__ == '__main__':
    extract = Extract_from_file()
    print(extract.get_txs())
