import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from sklearn.cluster import KMeans
from utility import get_session_db

class Clusrering_anal(object):
	style.use('ggplot')

	def __init__(self, n_clusters = 2):
		self.n_clusters = n_clusters
		self.session = get_session_db()

	def _get_data(self):
		from random import randint
		return np.array([(randint(0, 9),randint(0, 9)) for i in range(9)])

	def _get_delta_gasPrice(self):
		sql = '''
            select
            	bck_time - received as delta,
            	gas_price / 1000000000
            from
                tx
            natural join
                block
            where
                bck_time > 0 
                and delta < 4000
                limit 1000;
                -- received > %d and
                -- received < %d and
        ''' 
		return np.array([row for row in self.session.execute(sql)])

	def _set_centroids(self, X):
		clf = KMeans(n_clusters = self.n_clusters)
		clf.fit(X)
		self.colors = ['g.', 'r.', 'c.', 'b.', 'k.', 'o.']
		self.labels = clf.labels_
		self.centroid = clf.cluster_centers_

	def _set_plot(self, X):
		self._set_centroids(X)
		for i in range(len(X)):
			plt.plot(X[i][0], X[i][1], self.colors[self.labels[i]], markersize = 10)
		plt.scatter(self.centroid[:,0], self.centroid[:,1], marker = 'x', s = 5, linewidths = 5)

	def show_scatter(self):
		self._set_plot(self._get_delta_gasPrice())
		plt.show()


if __name__ == '__main__':
	ca = Clusrering_anal(n_clusters = 5)
	ca.show_scatter()
