from load import Load

class Extract_block:

    def __init__(self):
        self.load = Load()

    


if __name__ == '__main__':
    load = Load()
    print(load.get_hashes_without_block_id())
