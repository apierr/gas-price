# It will look at gasprices over the last 100 * 12 seconds
# and provide gas price estimates based on different predictive model
import re, csv, random
from session_db import get_session_db

class Smart_gas:

    def __init__(self, **kwargs):
        self.session = get_session_db()
        self.points = kwargs['points']
        self.block_time = kwargs['block_time']
        self.wating_time = kwargs['wating_time']
        self.max_time = self._get_max_timestamp()
        self.min_time = self.max_time - (self.points * self.block_time)

    def _get_the_delta_vs_gas_price(self, oracle_price):
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
            if row[0] > self.wating_time:
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
        ''' % (self.min_time, self.max_time)
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
                    avg(gas_price/1000000000) as y
                from
                    tx natural join block
                where
                    bck_time > 0 and
                    received > %d and
                    received < %d and
                    -- bck_time - received > 0 and
                    bck_time - received < %d
            ''' % (ts, ts, ts + self.block_time, self.wating_time)
        return re.sub('^UNION', '', sql)

    def _get_gas(self):
        sql = ''
        for ts in self._get_range_interval():
            sql += '''UNION
                select
                    %d as x,
                    gas_price/1000000000 as y
                from
                    tx natural join block
                where
                    bck_time > 0 and
                    received > %d and
                    received < %d and
                    -- bck_time - received > 0 and
                    bck_time - received < %d
            ''' % (ts, ts, ts + self.block_time, self.wating_time)
        return re.sub('^UNION', '', sql)

    def _get_max_timestamp(self):
        sql = '''
            select max(file_timestamp) from tx;
        '''
        return 1539707160

    def _get_range_interval(self):
        return list(range(self.min_time, self.max_time, self.block_time))

    def _get_query_result(self):
        dataset = []
        for row in self.session.execute(self._get_avg_gas()):
            if row['y']:
                dataset.append([row['x'], row['y']])
        return dataset

    def _get_train_and_test_data(self):
        data = self._get_query_result()
        random.shuffle(data)
        data_len = len(data)
        return {
            'train_data': data[:int(data_len/2)],
            'test_data': data[int(data_len/2):],
            'gas_oracle_ethchain': self._get_gas_oracle_ethchain()
        }

    def _write_cvs(self, key, value):
        with open(key + '.csv', mode = 'w') as date_file:
            writer = csv.writer(date_file, delimiter = '|')
            writer.writerow(['x', 'y'])
            for row in value:
                writer.writerow(row)
        print('The data are in: ' + key + '.csv')

    def write_csv(self):
        train_and_test_data = self._get_train_and_test_data()
        for data in train_and_test_data:
            self._write_cvs(data, train_and_test_data.get(data))

if __name__ == '__main__':
    smart_gas = Smart_gas(**{
        'points': 400,
        'block_time': 12,
        'wating_time': 60
    })
    smart_gas.write_csv()
    # smart_gas._get_the_delta_vs_gas_price(5000000000)
    # print(smart_gas._get_gas_oracle_ethchain())
