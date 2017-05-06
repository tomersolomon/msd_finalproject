
# data analysis source: http://infolab.stanford.edu/~west1/pubs/West-Leskovec_WWW-12.pdf

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def getpathData():
	def myencode(strList):
		return [x.encode('utf-8') for x in strList]

	paths_fin_df = pd.read_csv("../data/wikispeedia_paths-and-graph/paths_finished.tsv", 
							sep='\t', header=None, 
	names=["hashedIpAddress", "timestamp", "durationInSec", "path","rating"], 
	skip_blank_lines=True, comment='#', encoding='utf-8')

	# split path variable and encode each string in series of list of strings
	paths_fin_df["path"] = paths_fin_df["path"].str.split(pat=';')
	paths_fin_df["path"] = paths_fin_df["path"].apply(myencode)
	paths_fin_df['pathlength'] = paths_fin_df["path"].apply(len)
	getSource = lambda l: l[0] 
	getTarget = lambda l: l[-1] 
	getSource_Target = lambda l: l[0] + "|" + l[-1]
	paths_fin_df['source'] =  paths_fin_df['path'].apply(getSource)
	paths_fin_df['target'] = paths_fin_df['path'].apply(getTarget)
	paths_fin_df['source_target'] = paths_fin_df['path'].apply(getSource_Target)
	return paths_fin_df

def gen_histogram(paths_fin_df):
	fig = plt.figure()
	axes = fig.add_subplot(1,1,1)
	paths_fin_df['pathlength'].plot(kind='hist', ax=axes,logy=True, xlim=(0,150), bins=50)
	axes.set_xlabel("path-length")
	axes.set_ylabel("frequency")
	plt.savefig('../plots/histogram_click_freq.pdf')


def shortest_path_analysis(df):
	
	# calculate cumulative frequency of shortest possible path
	freq_sh_paths = df['path_length'].value_counts(sort=True).to_frame()
	freq_sh_paths.columns=['shortest_path_counts']
	freq_sh_paths['path_length'] =  freq_sh_paths.index
	freq_sh_paths = freq_sh_paths.reset_index()
	freq_sh_paths = freq_sh_paths.sort_values('path_length')

	freq_sh_paths['cum_sum'] = freq_sh_paths.shortest_path_counts.cumsum()
	freq_sh_paths['cum_perc'] = freq_sh_paths.cum_sum / freq_sh_paths.shortest_path_counts.sum()
	freq_sh_paths['perc'] = freq_sh_paths.shortest_path_counts / freq_sh_paths.shortest_path_counts.sum()
	return freq_sh_paths

def pathsWithBackAnalysis(paths_fin_df):
	# calculate and plot cumulative frequency of 
	# effective paths taken
	freq_paths = paths_fin_df['pathlength'].value_counts(sort=True).to_frame()
	freq_paths.columns=['path_counts']
	freq_paths['pathlength'] =  freq_paths.index
	freq_paths = freq_paths.reset_index()
	freq_paths = freq_paths.sort_values('pathlength')
	
	freq_paths['cum_sum'] = freq_paths.path_counts.cumsum()
	freq_paths['cum_perc'] = freq_paths.cum_sum /     freq_paths.path_counts.sum()
	freq_paths['perc'] = freq_paths.path_counts / freq_paths.path_counts.sum()
	return freq_paths

def effectivePathAnalysis(paths_fin_df):
	
	def removeBack(l):
		l = [x for x in l if x != '<']
		return l
	# show which rows contain '<' in 'path' column and get that subset
	effective_paths_df = paths_fin_df[paths_fin_df.path.map(lambda x: '<' in x) ]
	effective_paths_df = effective_paths_df.rename(columns = {'pathlength':'effective_path_length'})
	effective_paths_df['path'] = effective_paths_df['path'].apply(removeBack)	
	effective_paths_df['effective_path_length'] = effective_paths_df['path'].apply(len)
	tmp = paths_fin_df
	tmp.loc[tmp.hashedIpAddress.isin(effective_paths_df.hashedIpAddress), ['path', 'pathlength']] = \
			effective_paths_df[['path', 'effective_path_length']]
	effective_paths_df = tmp
	effective_paths_df = effective_paths_df.rename(columns = {'pathlength':'effective_path_length'})

	# calculate and plot cumulative frequency of 
	# effective paths taken
	freq_eff_paths = effective_paths_df['effective_path_length'].value_counts(sort=True).to_frame()
	freq_eff_paths.columns=['eff_path_counts']
	freq_eff_paths['pathlength'] =  freq_eff_paths.index
	freq_eff_paths = freq_eff_paths.reset_index()
	freq_eff_paths = freq_eff_paths.sort_values('pathlength')
	
	freq_eff_paths['cum_sum'] = freq_eff_paths.eff_path_counts.cumsum()
	freq_eff_paths['cum_perc'] = freq_eff_paths.cum_sum / freq_eff_paths.eff_path_counts.sum()
	freq_eff_paths['perc'] = freq_eff_paths.eff_path_counts / freq_eff_paths.eff_path_counts.sum()

	return effective_paths_df, freq_eff_paths

def genFreqDistPlots(freq_sh_paths, freq_eff_paths, freq_back_paths):
	fig = plt.figure(figsize=(15,8))
	axes = fig.add_subplot(1,1,1)
	axes.loglog(freq_sh_paths['path_length'], freq_sh_paths['perc'], '-ko', label='optimal')
	axes.loglog(freq_eff_paths['pathlength'], freq_eff_paths['perc'], '-ro', label='effective')
	axes.loglog(freq_back_paths['pathlength'], freq_back_paths['perc'], '-bo', label='complete')
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	axes.legend(loc=1)
	plt.savefig('../plots/path_freq.pdf')


def main():

	# 1. read in data
	# read in list of wiki articles used in dataset
	articles_df = pd.read_csv("../data/wikispeedia_paths-and-graph/mod-articles.tsv", 
		skip_blank_lines=True, comment='#')
	# number of different articles (4604)
	numArticles = len(articles_df)
	
	# get data from all users that completed wikispeedia paths
	paths_fin_df = getpathData()
	st_paths_df = pd.DataFrame( paths_fin_df.groupby(['source', 'target']).size() )
	

	# ========================================================================
	# 2. generate frequency distribution plots

	# read in matrix of shortest possible paths from one wiki article to next
	shortest_p = np.loadtxt("../data/wikispeedia_paths-and-graph/mod-shortest-path-distance-matrix.txt",
	 	comments='#')
	shortest_p_df = pd.DataFrame(data=shortest_p, index = articles_df['articles'], columns=articles_df['articles'])
	df_shortest_p = pd.DataFrame(data=shortest_p.reshape(shortest_p.shape[0]**2), columns=['path_length'])

	# generate histogram of number of clicks in completed paths
	gen_histogram(paths_fin_df)
	
	# different types of path lengths based on different pathlength criteria
	freq_back_paths = pathsWithBackAnalysis(paths_fin_df)
	freq_sh_paths  = shortest_path_analysis(df_shortest_p)
	effective_paths_df, freq_eff_paths =  effectivePathAnalysis(paths_fin_df)
	# ========================================================================

	# generate frequency distribution plots 
	genFreqDistPlots(freq_sh_paths, freq_eff_paths, freq_back_paths)
	
	# analyze only those users who have source-target path of a certain optimal path length
	def getOptPath(source, target, data):
		return data.loc[source, target]
	def rowFunction(row, data=None):
		if data is not None:
			return getOptPath(row['source'], row['target'], data )

	paths_fin_df['opt_path_length'] = paths_fin_df.apply( rowFunction, data=shortest_p_df , axis=1)
	path3 = paths_fin_df.loc[paths_fin_df["opt_path_length"] == 3]
	path4 = paths_fin_df.loc[paths_fin_df["opt_path_length"] == 4]
	path5 = paths_fin_df.loc[paths_fin_df["opt_path_length"] == 5]
	path6 = paths_fin_df.loc[paths_fin_df["opt_path_length"] == 6]

	# get summary statistics
	print( path3["pathlength"].describe() )
	print( path4["pathlength"].describe() )
	print( path5["pathlength"].describe() )
	print( path6["pathlength"].describe() )

	# calculate frequency values for all paths that have a certain optimal path length
	freq3 = path3['pathlength'].value_counts(sort=True).to_frame()
	freq3.columns = ['path_counts']
	freq3['pathlength'] =  freq3.index
	freq3 = freq3.reset_index()
	freq3 = freq3.sort_values('pathlength')
	freq3['cum_sum']  = freq3.path_counts.cumsum()
	freq3['cum_perc'] = freq3.cum_sum / freq3.path_counts.sum()
	freq3['perc']     = freq3.path_counts / freq3.path_counts.sum()

	freq4 = path4['pathlength'].value_counts(sort=True).to_frame()
	freq4.columns = ['path_counts']
	freq4['pathlength'] =  freq4.index
	freq4 = freq4.reset_index()
	freq4 = freq4.sort_values('pathlength')
	freq4['cum_sum']  = freq4.path_counts.cumsum()
	freq4['cum_perc'] = freq4.cum_sum / freq4.path_counts.sum()
	freq4['perc']     = freq4.path_counts / freq4.path_counts.sum()
	
	freq5 = path5['pathlength'].value_counts(sort=True).to_frame()
	freq5.columns = ['path_counts']
	freq5['pathlength'] =  freq5.index
	freq5 = freq5.reset_index()
	freq5 = freq5.sort_values('pathlength')
	freq5['cum_sum']  = freq5.path_counts.cumsum()
	freq5['cum_perc'] = freq5.cum_sum / freq5.path_counts.sum()
	freq5['perc']     = freq5.path_counts / freq5.path_counts.sum()
	
	freq6 = path6['pathlength'].value_counts(sort=True).to_frame()
	freq6.columns = ['path_counts']
	freq6['pathlength'] =  freq6.index
	freq6 = freq6.reset_index()
	freq6 = freq6.sort_values('pathlength')
	freq6['cum_sum']  = freq6.path_counts.cumsum()
	freq6['cum_perc'] = freq6.cum_sum / freq6.path_counts.sum()
	freq6['perc']     = freq6.path_counts / freq6.path_counts.sum()

	fig = plt.figure()
	
	axes = fig.add_subplot(1,1,1)
	axes.plot(freq3['pathlength'], freq3['perc'], 'ro-', label='opt3')
	axes.plot(freq4['pathlength'], freq4['perc'], 'ko-', label='opt4')
	axes.plot(freq5['pathlength'], freq5['perc'], 'bo-', label='opt5')
	
	axes.set_xlim(0, 20)
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	axes.legend(loc=2)
	
	plt.savefig('../plots/opt3-opt4-opt5.pdf')





if __name__ == "__main__":
	main()

