
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

def gen_plots(paths_fin_df):
	fig = plt.figure()
	axes = fig.add_subplot(1,1,1)
	paths_fin_df['pathlength'].plot(kind='hist', ax=axes,logy=True, xlim=(0,150), bins=50)
	axes.set_xlabel("path-length")
	axes.set_ylabel("frequency")
	plt.savefig('../plots/histogram_click_freq.pdf')

def main():
	# get path data
	#paths_fin_df = getpathData()
	#gen_plots(paths_fin_df)

	# read in list of wiki articles used in dataset
	#articles_df = pd.read_csv("../data/wikispeedia_paths-and-graph/mod-articles.tsv", skip_blank_lines=True, comment='#')
	
	# number of different articles (4604)
	#numArticles = len(articles_df)
	# read in matrix of shortest possible paths from one wiki article to next
	shortest_p = np.loadtxt("../data/wikispeedia_paths-and-graph/mod-shortest-path-distance-matrix.txt",
		comments='#')
	df = pd.DataFrame(data=shortest_p.reshape(shortest_p.shape[0]**2), columns=['path_length'])

	# calculate and plot cumulative frequency of shortets possible path
	freq_sh_paths = df['path_length'].value_counts(sort=True).to_frame()
	freq_sh_paths.columns=['shortest_path_counts']
	freq_sh_paths['path_length'] =  freq_sh_paths.index
	freq_sh_paths = freq_sh_paths.reset_index()
	freq_sh_paths = freq_sh_paths.sort_values('path_length')

	freq_sh_paths['cum_sum'] = freq_sh_paths.shortest_path_counts.cumsum()
	freq_sh_paths['cum_perc'] = freq_sh_paths.cum_sum / freq_sh_paths.shortest_path_counts.sum()
	freq_sh_paths['perc'] = freq_sh_paths.shortest_path_counts / freq_sh_paths.shortest_path_counts.sum()
	print(freq_sh_paths)

	fig = plt.figure()
	axes = fig.add_subplot(1,2,1)
	axes.loglog(freq_sh_paths['path_length'], freq_sh_paths['cum_perc'])
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	axes.set_title('cumulative percentage')
	
	axes = fig.add_subplot(1,2,2)
	axes.loglog(freq_sh_paths['path_length'], freq_sh_paths['perc'], 'k')
	axes.set_xlabel('number of clicks')
	axes.set_ylabel('percentage')
	plt.savefig('../plots/shortest_path_freq.pdf')



if __name__ == "__main__":
	main()

