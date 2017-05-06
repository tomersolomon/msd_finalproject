
from __future__ import print_function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn 

def getOptPath(source, target, data):
	return data.loc[source, target]

def rowFunction(row, data=None, col = None):
	if data is not None and col is None:
		return getOptPath(row['source'], row['target'], data )		
	elif data is not None and col is not None and row[col] is not None:
		return getOptPath(row[col], row['target'], data )		

def getpathData():
	def myencode(strList):
		return [x.encode('utf-8') for x in strList]
	paths_fin_df = pd.read_csv("../data/wikispeedia_paths-and-graph/paths_finished.tsv", 
			sep='\t', header=None, names=["hashedIpAddress", "timestamp", "durationInSec", "path","rating"], 
			skip_blank_lines=True, comment='#', encoding='utf-8')
	paths_fin_df["path"] = paths_fin_df["path"].str.split(pat=';')
	paths_fin_df["path"] = paths_fin_df["path"].apply(myencode)
	paths_fin_df['pathlength'] = paths_fin_df["path"].apply(len)
	
	getSource = lambda l: l[0] 
	getTarget = lambda l: l[-1] 
	getSource_Target = lambda l: l[0] + "|" + l[-1]

	paths_fin_df['source'] =  paths_fin_df['path'].apply(getSource)
	paths_fin_df['target'] = paths_fin_df['path'].apply(getTarget)
	paths_fin_df['source_target'] = paths_fin_df['path'].apply(getSource_Target)
	
	articles_df = pd.read_csv("../data/wikispeedia_paths-and-graph/mod-articles.tsv", 
		skip_blank_lines=True, comment='#')
	shortest_p = np.loadtxt("../data/wikispeedia_paths-and-graph/mod-shortest-path-distance-matrix.txt",
	 	comments='#')
	shortest_p_df = pd.DataFrame(data=shortest_p, index = articles_df['articles'], columns=articles_df['articles'])
	df_shortest_p = pd.DataFrame(data=shortest_p.reshape(shortest_p.shape[0]**2), columns=['path_length'])


	paths_fin_df['opt_path_length'] = paths_fin_df.apply( rowFunction, data=shortest_p_df , axis=1)

	return paths_fin_df, shortest_p_df

def main():
	paths_fin_df, shortest_p_df = getpathData()
	paths_fin_df = paths_fin_df[paths_fin_df.durationInSec != 0 ]
	def get2state(l):
		return l[1]
	def get3state(l):
		if len(l) > 2:
			return l[2];
		else: 
			return None

	def removeBack(l):
		l = [x for x in l if x != '<']
		return l
	# show which rows contain '<' in 'path' column and get that subset
	paths_fin_df2 = paths_fin_df

	paths_fin_df2['path'] = paths_fin_df2['path'].apply(removeBack)	
	paths_fin_df2['state2'] =  paths_fin_df2['path'].apply(get2state)
	paths_fin_df2['state3'] =  paths_fin_df2['path'].apply(get3state)
	paths_fin_df2['opt2path_length'] = paths_fin_df2.apply( rowFunction, 
										data=shortest_p_df, col='state2' , axis=1)
	paths_fin_df2['opt3path_length'] = paths_fin_df2.apply( rowFunction, 
										data=shortest_p_df, col='state3' , axis=1)
	paths_fin_df.to_csv("../task-data/data_with_optimal.csv")

	stats_df = paths_fin_df2[['path', 'state2', 'opt_path_length','opt2path_length', 'opt3path_length' ]]
	stats_df['ratio1'] = stats_df['opt2path_length'] / stats_df['opt_path_length'] 
	stats_df['ratio2'] = stats_df['opt3path_length'] / stats_df['opt_path_length'] 
	
	fig = plt.figure(figsize=(10,7))
	axes = fig.add_subplot(1,2,1)
	axes.set_xlabel('Ratio')
	axes.set_ylabel('frequency')
	axes.set_title('2 ST. to Target-OP over original OP')
	stats_df['ratio1'].plot(kind='hist', ax=axes, logy=True, bins=40)

	axes = fig.add_subplot(1,2,2)
	axes.set_xlabel('Ratio')
	axes.set_ylabel('frequency')
	axes.set_title('3 ST to Target-OP over original OP')
	stats_df['ratio2'].plot(kind='hist', ax=axes, logy=True, bins=40)
	plt.savefig("../plots/optimal_path_ratios.pdf")

if __name__ == "__main__":
	main()





