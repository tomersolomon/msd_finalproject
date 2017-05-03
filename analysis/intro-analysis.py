
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

	return freq_eff_paths

def genFreqDistPlots(freq_sh_paths, freq_eff_paths):
	fig = plt.figure()
	axes = fig.add_subplot(1,2,1)
	axes.loglog(freq_sh_paths['path_length'], freq_sh_paths['cum_perc'])
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	axes.set_title('cumulative percentage')
	
	axes = fig.add_subplot(1,2,2)
	axes.loglog(freq_sh_paths['path_length'], freq_sh_paths['perc'], '-ko')
	axes.loglog(freq_eff_paths['pathlength'], freq_eff_paths['perc'], '-o')
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	plt.savefig('../plots/path_freq.pdf')

	


def main():
	# read in list of wiki articles used in dataset
	articles_df = pd.read_csv("../data/wikispeedia_paths-and-graph/mod-articles.tsv", 
		skip_blank_lines=True, comment='#')
	# number of different articles (4604)
	numArticles = len(articles_df)

	# ================================================================
	# get data from all users that completed wikispeedia paths
	paths_fin_df = getpathData()

	# read in matrix of shortest possible paths from one wiki article to next
	shortest_p = np.loadtxt("../data/wikispeedia_paths-and-graph/mod-shortest-path-distance-matrix.txt",
		comments='#')
	df_shortest_p = pd.DataFrame(data=shortest_p.reshape(shortest_p.shape[0]**2), columns=['path_length'])

	# generate histogram of number of clicks in completed paths
	gen_histogram(paths_fin_df)
	# ================================================================
	
	# different types of path lengths based on different pathlength criteria
	freq_sh_paths  = shortest_path_analysis(df_shortest_p)
	freq_eff_paths =  effectivePathAnalysis(paths_fin_df)

	# generate frequency distribution plots 
	genFreqDistPlots(freq_sh_paths, freq_eff_paths)



if __name__ == "__main__":
	main()

