from utility import get_session_db, get_engine
import pandas as pd
import numpy as np 

class Query:

	def __init__(self, **kwarg):
		self.tstart = kwarg['tstart']
		self.tstop = kwarg['tstop']

	def _get_timeFrame(self):
		return '''
			file_timestamp > %d AND
			file_timestamp < %d
			ORDER by file_timestamp
		''' % (self.tstart, self.tstop)

	def get_gasLimit_gasPrice_deltaCategory(self, rowNumber = 100000):
		sql = '''
			SELECT 
				received,
			    bck_time - received as waiting_time_s,
				gas_limit as gas_limit, 
				gas_price / 1000000000 as gas_price_gWei,
				CASE
					WHEN (bck_time - received) < 0
						THEN 'negative_time'
					WHEN (bck_time - received) >= 0 and (bck_time - received) <= 60
						THEN 'less_1_min' 
					WHEN (bck_time - received) > 60 and (bck_time - received) <= 60 * 3
						THEN 'between_1_and_3_min' 
					WHEN  (bck_time - received) > 60 * 3 
						THEN 'greater_3_min'
			          -- ELSE 0
				END category,
				CASE
					WHEN (bck_time - received) < 0
						THEN -1
					WHEN (bck_time - received) >= 0 and (bck_time - received) <= 60
						THEN 0 
					WHEN (bck_time - received) > 60 and (bck_time - received) <= 60 * 3
						THEN 1
					WHEN  (bck_time - received) > 60 * 3 
						THEN 3
			          -- ELSE 0
				END categoryNumber
			FROM 
				tx natural join block 
			WHERE 
				bck_id > 0 AND
				gas_limit < 500000 AND
				gas_price_gWei < 50
			LIMIT %d ;
		''' % (rowNumber)
		return pd.read_sql_query(sql, get_engine())

	def get_usd(self):
		sql = '''
			SELECT
				file_timestamp as unix_ts, 
				usd 
			FROM networkstats
			WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

	def get_btc(self):
		sql = '''
			SELECT
				file_timestamp as unix_ts, 
				btc 
			FROM networkstats
			WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

	def get_miners(self):
		sql = '''
			SELECT
				file_timestamp as unix_ts, 
				-- strftime('%d-%H:%M:%S', datetime(file_timestamp, 'unixepoch')) as unix_ts,
				hashRate 
			FROM poolstats
			WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

	def get_difficulty(self):
		sql = '''
			SELECT 
				file_timestamp as unix_ts, 
				difficulty
			FROM networkstats WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

	def get_gasPrice(self):
		sql = '''
			SELECT
				file_timestamp as unix_ts,
				fastest as Price_GWei
			FROM gasoracleethchain WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

	def get_pending_txs(self):
		sql = '''
			SELECT
				file_timestamp as unix_ts,
				unconfirmed_count as pending_tx
			FROM memoryPool WHERE
		''' + self._get_timeFrame()
		return pd.read_sql_query(sql, get_engine())

if __name__ == '__main__':
	q = Query()
	print(q.get_gasLimit_gasPrice_deltaCategory().head())