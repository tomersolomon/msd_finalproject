
task-data dir
This directory contains data tables created by our programs.  

plaintext_articles dir
The plaintext_articles directory contains a list of plain-txt files of all the articles used in the wikispeedia dataset.  

wikispeedia_paths-and-graph
1. articles.tsv: tab seperated value txt file that contains a list of article names.  
2. mod-articles.tsv: contains a modified version of articles.tsv that we created by manually deleting the first few lines that start with '#'. 
3. categories.tsv: file maps all articles to a list of hierarchally-structured categories:
4. links.tsv: contains a list of all directed edges in the network in alphabetical order.  
5. shortest-path-distance-matrix.txt: file is a numArticles by numArticles square matrix in which a row contains the distances from the source to all articles (targets of the shortest path).
6. mod-shortest-path-distance-matrix.txt: is a modified outputted version of the above file.  I manulaly deleted all comments in the top of the original file (those that start with '#').  Afterwards, I ran two linux commands (tr and sed) to insert a space between each value in the matrix (for reading it as an input file). 
7. paths_finished.tsv:   contains completed paths
8. paths_unfinished.tsv: contains uncompleted paths
9. 