
# data analysis source: http://infolab.stanford.edu/~west1/pubs/West-Leskovec_WWW-12.pdf

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns




def getData():
	def myencode(strList):
		return [x.encode('utf-8') for x in strList]

	paths_fin_df = pd.read_csv("../data/wikispeedia_paths-and-graph/paths_finished.tsv", 
	sep='\t', header=None, 
	names=["hashedIpAddress", "timestamp", "durationInSec", "path","rating"], skip_blank_lines=True, comment='#', encoding='utf-8')

	# split path variable and encode each string in series of list of strings
	paths_fin_df["path"] = paths_fin_df["path"].str.split(pat=';')
	paths_fin_df["path"] = paths_fin_df["path"].apply(myencode)
	paths_fin_df['pathlength'] = paths_fin_df["path"].apply(len)
	return paths_fin_df

def main():
	paths_fin_df = getData()
	print(paths_fin_df.head(n=10))

if __name__ == "__main__":
	main()

