library('tidyverse')
library('ggplot2')

####################################
# Number of links per article
####################################

# load file
read.delim("../data/wikispeedia_paths-and-graph/links.tsv", skip = 11, header = F) -> links
c("article", "link") -> colnames(links)
head(links)

# count number of links for each article
count(links, article) -> links_counted
c("article", "num_links") -> colnames(links_counted)
head(links_counted)

####################################
# Number of words per article
####################################

# create empty column for number of words for each article
mutate(links_counted, num_words = 0) -> article_summary

# For each article
for (k in 1:nrow(article_summary)) {
  
  # load file
  as.matrix(article_summary)[k, "article"] -> article_name
  paste("../data/plaintext_articles/",article_name,".txt", sep = "") -> file_name
  read_file(file_name) -> file
  
  # separate words
  strsplit(file, split = " ") -> words
  
  # count words and put into column
  length(words[[1]]) -> article_summary[k, "num_words"]
  
}

head(article_summary)

####################################
# Regression
####################################

# regress num of links~num words for each article
lm(article_summary$num_links~article_summary$num_words) -> fit
summary(fit)

####################################
# Plot
####################################

# linear scale
ggplot(article_summary, aes(x = num_words, y = num_links)) +
  geom_point() +
  labs(x = "Number of words", y = "Number of links", title = "Article Connections")

# log scale 
ggplot(article_summary, aes(x = num_words, y = num_links)) +
  geom_point() +
  scale_y_continuous(trans = 'log10') +
  scale_x_continuous(trans = 'log10') +
  labs(x = "Number of words", y = "Number of links", title = "Article Connections")
