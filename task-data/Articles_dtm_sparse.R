setwd("C:/Users/jverm/Dropbox/~S8 - Social/Project")
setwd("C:/cygwin64/home/jverm/GitHub/msd_finalproject/data/plaintext_articles")
library('tidyverse')
library('ggplot2')
library(tm)	
library(Matrix)
library(glmnet)
library(ROCR)

####################################
# Number of links per article
####################################

# load file
read.delim("mod_links.tsv", header = F) -> links
c("article", "link") -> colnames(links)
head(links)

# count number of links for each article
count(links, article) -> links_counted
c("article", "num_links") -> colnames(links_counted)
head(links_counted)

####################################
# Words in each article
####################################

# create empty column for number of words for each article
mutate(links_counted, words = 0) -> article_summary

# For each article
for (k in 1:nrow(article_summary)) {
  
  # load file
  as.matrix(article_summary)[k, "article"] -> article_name
  paste(article_name,".txt", sep = "") -> file_name
  read_file(file_name) -> file
  file -> article_summary[k, "words"]
  
}

View(article_summary)

####################################
# Creating the sparse matrix
####################################

# create a Corpus from the article words
Corpus(VectorSource(article_summary$words)) -> corpus

# remove punctuation and numbers
tm_map(corpus, removePunctuation) -> corpus
tm_map(corpus, removeNumbers) -> corpus

# create a DocumentTermMatrix from the snippet Corpus
DocumentTermMatrix(corpus) -> dtm
article_summary$article -> row.names(dtm)

# convert the DocumentTermMatrix to a sparseMatrix, required by cv.glmnet
# helper function
dtm_to_sparse <- function(dtm) {
  sparseMatrix(i=dtm$i, j=dtm$j, x=dtm$v, dims=c(dtm$nrow, dtm$ncol), dimnames=dtm$dimnames)
}

dtm_to_sparse(dtm) -> sparse
head(sparse)
