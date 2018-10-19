# It will look at gasprices over the last 100 * 12 seconds
# and provide gas price estimates based on different predictive model

class Smart_gas:

    def __init__(self):
        self.interval = 12
        self.range = 100

    def _get_gas(self):
        return '''
        select
            avg(gas_price)
        from
            tx natural join block
        where bck_time > 0 and
            bck_time - received > 0 and
            bck_time - received < 60;
        '''

    def extract_data(self):
        pass
