import metadata_db
from utility import get_json_from_file, get_files

class Open_block:

    def __init__(self):
        self.pattern = './output/*_block.json'

    def _get_class_attributes(self, cls):
        return [i[4:] for i in cls.__dict__.keys() if i[:1] != '_'][1:-1]

    def _get_files(self):
        return glob.glob(self.pattern)

    def network_stats(self):
        networks = []
        cls_attributes = ['height'] + self._get_class_attributes(metadata_db.Block)

        return networks

    def get_blocks(self):
        blocks = []
        cls_attributes = ['height'] + self._get_class_attributes(metadata_db.Block)
        for file in get_files(self.pattern):
            bck = get_json_from_file(file)
            if bck:
                blocks.append([bck[i] for i in  cls_attributes])
        return blocks

if __name__ == '__main__':
    open = Open_block()
    print(open.get_blocks())
