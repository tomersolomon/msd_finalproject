
task-data dir
This directory contains data tables created by our programs.  

plaintext_articles dir
The plaintext_articles directory contains a list of plain-txt files of all the articles used in the wikispeedia dataset.  

wikispeedia_paths-and-graph
1. articles.tsv: tab seperated value txt file that contains a list of article names.  
2. categories.tsv: file maps all articles to a list of hierarchally-structured categories:
3. links.tsv: contains a list of all directed edges in the network in alphabetical order.  
4. shortest-path-distance-matrix.txt: file is a numArticles by numArticles square matrix in which a row contains the distances from the source to all articles (targets of the shortest path).
5. mod-shortest-path-distance-matrix.txt: is a modified outputted version of the above file.  I manulaly deleted all comments in the top of the original file (those that start with '#').  Afterwards, I ran two linux commands (tr and sed) to insert a space between each value in the matrix (for reading it as an input file). 
6. paths_finished.tsv:   contains completed paths (raw data)
7. paths_unfinished.tsv: contains uncompleted paths (raw data)


*** modify-shortest-path-distance-matrix.sh is a shell script which is run by typing ./modify-shortest-path-distance-matrix.sh in the command line.  Make sure you have executable permissions to run (see chmod function for details).  More importantly, do not pass in any command line arguments as this script has hard coded the file it will read.  This shill script produces the mod-shortest-path-distance-matrix.txt file