# It will look at gasprices over the last 100 * 12 seconds
# and provide gas price estimates based on different predictive model
import re, csv, random
from session_db import get_session_db
from smart_gas_lm import Smart_gas_lm

class Smart_gas:

    def __init__(self, **kwargs):
        self.BLOCK_TEST = kwargs['block_test'] # number of blocks to test
        self.BLOCK_TRAIN = kwargs['block_train'] # number of blocks to train
        self.BLOCK_TIME = kwargs['block_time']
        self.START_TIME = kwargs['start_time']
        self.WAITING_TIME = kwargs['waiting_time']
        self.min_time = self.START_TIME - (self.BLOCK_TIME * self.BLOCK_TRAIN)
        self.max_time = self.START_TIME
        self.session = get_session_db()
        #self.min_time = self.max_time - (self.points * self.BLOCK_TIME)
        self.set_dataset()

    def _get_delta_vs_gas_price(self, oracle_price):
        sql = '''
            select
                bck_time - received
            from
                tx
            natural join
                block
            where
                bck_time > 0 and
                received > %d and
                received < %d and
                gas_price >= %d
        ''' % (self.min_time, self.max_time, oracle_price)
        print (sql)
        result = {'over': 0, 'under': 0}
        for row in self.session.execute(sql):
            if row[0] > self.WAITING_TIME:
                result['over'] += 1
            else:
                result['under'] += 1
        print(result)

    def _get_gas_oracle_ethchain(self):
        rows = []
        sql = '''
            select
                file_timestamp,
                fast
            from
                gasoracleethchain
            where
                file_timestamp > %d AND
                file_timestamp <  %d
        ''' % (self.START_TIME, self.START_TIME + self.BLOCK_TEST * self.BLOCK_TIME)
        for row in self.session.execute(sql):
            if row[1]:
                rows.append(row)
        return rows

    def _get_avg_gas(self):
        sql = ''
        for ts in self._get_range_interval():
            sql += '''UNION
                select
                    %d as x,
                    min(gas_price/1000000000) as y
                from
                    tx natural join block
                where
                    bck_time > 0 and
                    received > %d and
                    received < %d and
                    -- bck_time - received > 0 and
                    bck_time - received < %d
            ''' % (ts, ts, ts + self.BLOCK_TIME, self.WAITING_TIME)
        return re.sub('^UNION', '', sql)

    def _get_gas(self):
        sql = ''
        for ts in self._get_range_interval():
            sql += '''UNION
                select
                    %d as x,
                    min(gas_price/1000000000) as y
                from
                    tx natural join block
                where
                    bck_time > 0 and
                    received > %d and
                    received < %d and
                    -- bck_time - received > 0 and
                    bck_time - received < %d
            ''' % (ts, ts, ts + self.BLOCK_TIME, self.wating_time)
        return re.sub('^UNION', '', sql)

    def _get_range_interval(self):
        return list(range(self.min_time, self.max_time, self.BLOCK_TIME))

    def _get_query_result(self):
        dataset = []
        for row in self.session.execute(self._get_avg_gas()):
            if row['y']:
                dataset.append([row['x'], row['y']])
        return dataset

    def _write_cvs(self, key, value):
        with open(key + '.csv', mode = 'w') as date_file:
            writer = csv.writer(date_file, delimiter = '|')
            writer.writerow(['x', 'y'])
            for row in value:
                writer.writerow(row)
        print('The data are in: ' + key + '.csv')

    def _sort_2d_list(self, _2d_list):
        return sorted(_2d_list, key = lambda l : l[1], reverse = False)

    def _remove_old_element_from_tmp_dataset(self):
        if self.dataset[0][0] < self.max_time - (self.BLOCK_TRAIN * self.BLOCK_TIME):
            self.dataset = self.dataset[1:]

    def _update_dataset(self):
        self.points = 1
        self.min_time = self.max_time
        self.max_time += self.BLOCK_TIME
        self._remove_old_element_from_tmp_dataset()
        new_value = self.session.execute(self._get_avg_gas()).first()
        if new_value[1]:
            self.dataset.append(new_value)
            self.full_dataset.append(new_value)

    def write_csv(self):
        for data in self.data:
            self._write_cvs(data, self.data.get(data))

    def _get_smart_gas(self):
        rows = []
        lm = Smart_gas_lm()
        timestamp = self.START_TIME
        for i in range(self.BLOCK_TEST):
            lm.set_train_dataset(self.dataset)
            timestamp += self.BLOCK_TIME
            smart_gas = lm.get_estiamte_value(timestamp)
            rows.append([timestamp, smart_gas])
            self._update_dataset()
        return rows

    def set_dataset(self):
        dataset = self._get_query_result()
        self.dataset = self._sort_2d_list(dataset)
        self.full_dataset = self.dataset
        random.shuffle(dataset)
        data_len = len(dataset)
        self.data = {
            'train_data': dataset[:int(data_len/2)],
            'test_data': dataset[int(data_len/2):],
            'gas_oracle_ethchain': self._get_gas_oracle_ethchain()
        }

    def write_datasets(self):
        datasets = {
            'smart_gas_ds': self._get_smart_gas(),
            'ether_gas_station_ds': self._get_gas_oracle_ethchain(),
            'test_ds': self.full_dataset
        }
        for dataset in datasets:
            self._write_cvs(dataset, datasets[dataset])

if __name__ == '__main__':
    sg = Smart_gas(**{
        'block_train': 200, # number of blocks to train
        'block_time': 12,
        'waiting_time': 60,
        'block_test': 1000, # number of blocks to test
        'start_time': 1539693600 # the test starts from this start_time
    })
    #sg._write_cvs('test_ds', sg.full_dataset)
    # print(sg.data['gas_oracle_ethchain'])
    # sg._get_smart_gas()
    sg.write_datasets()
