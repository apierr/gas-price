import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('ggplot')
import pymc3 as pm
from patsy import dmatrices
from query import Query as Q
from numpy.random import rand
from datetime import datetime
import seaborn as sns
import matplotlib.gridspec as gridspec
import config as cfg

# https://stackoverflow.com/questions/21192002/how-to-combine-2-plots-ggplot-into-one-plot

class Model_gas:

	def plt_scatter(self, formula, df):
		formula += ' -1'
		y, X = dmatrices(formula, df, return_type = 'dataframe')
		color = np.ravel(y)
		plt.scatter(X[X.columns[0]], X[X.columns[1]], alpha = 0.3, c = color, s = 20)
		plt.xlabel('gas_price (GWei)', fontsize = 12)
		plt.ylabel('gas_limit', fontsize = 12)
		cbar = plt.colorbar()
		cbar.set_label('waiting time (minutes)', rotation=270)
		plt.show()

	def _frequency_plot(self, formula, df):
		model = pm.Model()
		with model:
			pm.glm.GLM.from_formula(
				formula,
				data = df
			)
			start = pm.find_MAP()
			step = pm.NUTS(scaling = start)
			trace = pm.sample(2000, step, prograssbar = True)
		plt.figure(figsize = (7, 7))
		pm.traceplot(trace[100:])
		plt.tight_layout()
		pm.summary(trace)
		plt.savefig('frequency-13-oct.png')

	def _get_xlabels(self, x):
		return [i for i in x if i % 3600 == 0 or (i - 1)% 3600 == 0]

	def _get_hDate(self, ts):
		return datetime.utcfromtimestamp(ts).strftime('%H:%M')

	def set_plots(self, dfs = []):
		fig = plt.figure()
		x = self._get_xlabels(dfs[0]['unix_ts'])
		labels = [self._get_hDate(ts) for ts in x]

		for i, df in enumerate(dfs):
			cols = list(df)
			ax = fig.add_subplot(len(dfs), 1, i + 1)
			ax.plot(df[cols[0]], df[cols[1]])
			# ax.set_xlabel(cols[0])
			ax.set_xticklabels([])
			ax.set_ylabel(cols[1])
		plt.xticks(x, labels, rotation = '45')
		plt.show()

	def density_estimation(self, **kwargs):
		cs = ['c', 'r', 'y', 'b']
		cats = df.category.unique()
		for i, c in enumerate(cats):
			d = kwargs['df'].loc[df['category'] == c]
			print(kwargs['df'].head())
			g = sns.jointplot(x = kwargs['x'], y = kwargs['y'], data = d, kind = 'hex', color = cs[i])
			plt.title(c)
			g.savefig(c + '.png')

	def heat_map_correlation(self):
		df = pd.read_csv(cfg.df_fn)
		# method parameter can be pearson, kendall, spearman
		# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.corr.html
		columns_name = ['btc', 'usd', 'pending_tx', 'Fastest_price']
		sns.heatmap(df[columns_name].corr(method = 'pearson', min_periods = 1), annot = True, fmt = '.2f')
		plt.show()

	def _drop_ts(self, df):
		# it drops the unix_timestamp columns
		try:
			return df.drop(['unix_ts'], axis=1)
		except:
			df = df.reset_index()
			return df.drop(['received'], axis = 1)

	def write_merged_df(self):
		dfs = [
			q.get_usd(),
			q.get_pending_txs(),
			q.get_btc(),
			q.get_gasPrice()
		]
		for i in range(len(dfs)):
			try:
				rs = rs.join(self._drop_ts(dfs[i]), how ='outer')
			except:
				rs = dfs[0]
		rs.unix_ts = rs.unix_ts.fillna(0).astype(int)
		rs.to_csv(cfg.df_fn)

if __name__ == '__main__':
	m = Model_gas()
	q = Q(**{
		'tstart': 1539561600, 
		'tstop': 1539561600 + (60 * 60 * 24)
	})
	# print(m._get_merge_df().head())
	m.write_merged_df()
	# m.heat_map_correlation()

	# print(q.get_delta_resample())
	#print((df.received.max() - df.received.min()).seconds)


	# m.set_plots([
	# 	q.get_gasPrice(), 
	# 	# q.get_difficulty(), 
	# 	q.get_pending_txs(), 
	# 	q.get_miners(),
	# 	q.get_usd(),
	# 	q.get_btc()
	# ])
	
	# df = q.get_gasLimit_gasPrice_deltaCategory()
	# # df = df.loc[df['category'] == 'negative_time']

	# # m.density_estimation(**{
	# # 	'df': df,
	# # 	'x': 'waiting_time_s', #'gas_limit'
	# # 	'y': 'gas_price_gWei'
	# # })

	# m.plt_scatter('categoryNumber ~ gas_price_gWei + gas_limit', df = q.get_gasLimit_gasPrice_deltaCategory())
