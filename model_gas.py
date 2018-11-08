import numpy as np 
import pandas as pd
from matplotlib import pyplot as plt
import pymc3 as pm
from ggplot import *
from patsy import dmatrices
from query import Query as Q
from numpy.random import rand

# https://stackoverflow.com/questions/21192002/how-to-combine-2-plots-ggplot-into-one-plot

class Model_gas:

	def _get_legend_markers(self, D_label_color, marker="o", marker_kws={"linestyle":""}):

		markers = [plt.Line2D([0,0],[0,0],color = color, marker = marker, **marker_kws) for color in D_label_color.values()]
		return (markers, D_label_color.keys())

	def create_data(self):
		N = 100
		beer = np.random.normal(loc = 0, scale = 1, size = N)
		warm = np.random.normal(loc = 0, scale = 1, size = N)
		family = np.random.randint(2, size = N)
		# linear combination
		z = 1 + 2 * beer + -3 * warm + .5 * family
		# invert-logit function
		pr = [1 / (1 + np.exp(-i)) for i in z]
		canada = np.random.binomial(1, p = pr, size = N)
		# fake family into factor
		family = np.where(family == 0, 'No', 'Yes')
		return canada, beer, warm, family  

	def get_df(self):
		canada, beer, warm, family = self.create_data()
		df =  pd.DataFrame({
			'canada': canada,
			'beer': beer,
			'warm': warm,
			'family': family
		})
		return df

	def to_csv(self, df):
		df.to_csv('canada.csv', index = False)

	def plt_scatter(self, formula, data = {}):
		formula += ' -1'
		y, X = dmatrices(formula, data, return_type = 'dataframe')
		color = np.ravel(y)	
		plt.scatter(X[X.columns[0]], X[X.columns[1]], alpha = 0.3, c = color, s = 20)
		plt.xlabel('gas_price (GWei)', fontsize = 12)
		plt.ylabel('gas_limit', fontsize = 12)
		cbar = plt.colorbar()
		cbar.set_label('waiting time (minutes)', rotation=270)
		plt.show()

	def frequency_plot(self, formula, df):
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

	def geom_step(self, df):
		return ggplot(aes(x = 'x'), data = df) +\
		    geom_line(aes(y = 'y'), color = 'blue') +\
		    geom_line(aes(y = 'z'), color = 'red')

if __name__ == '__main__':
	m = Model_gas()
	q = Q(**{
		'tstart': 1539561600, 
		'tstop': 1539561600 + 12 * 60 * 100
	})
	print(q.get_pending_tx().head())
	g1 = m.geom_step(df = q.get_pending_tx())
	print(g1)

	# g2 = m.geom_step(df = q.get_difficulty())
	

	# g.make()
	# fig = plt.gcf()
	# ax = plt.gca()
	# plt.show()


	# print(Q().get_gasLimit_gasPrice_deltaCategory(100))
	# m.plt_scatter('category ~ gWei + gas_limit', data = Q().get_gasLimit_gasPrice_deltaCategory(limit = 1000))

	# m.to_csv(m.get_df())
	# m.plt_scatter('canada ~ beer + warm', data = m.get_df())
	# m.frequency_plot('canada ~ beer + warm + family')
	# m.frequency_plot('category ~ gWei + gas_limit', Q().get_gasLimit_gasPrice_deltaCategory(limit = 100))
