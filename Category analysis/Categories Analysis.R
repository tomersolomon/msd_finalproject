setwd("C:/Users/jverm/Dropbox/~S8 - Social/Project")
library('tidyverse')
library('ggplot2')

####################################
# Step 1: Extract articles from paths
####################################

# load files
read.delim("mod_paths_unfinished.tsv", header = F) -> paths_unfin
head(paths_unfin)

read.delim("mod_paths_finished.tsv", header = F) -> paths_fin
head(paths_fin)

# select column with article paths
select(paths_unfin, V4) -> articles_unfin
head(articles_unfin)

select(paths_fin, V4) -> articles_fin
head(articles_fin)

# split into individual articles
split = function(x) strsplit(as.character(x), split = ";")
apply(articles_unfin, 1, split) -> split_articles_unfin
head(split_articles_unfin)

apply(articles_fin, 1, split) -> split_articles_fin
head(split_articles_fin)

####################################
# Step 2: Create category key
####################################

# load file
read.delim("mod_categories.tsv", header = FALSE) -> categories_map
head(categories_map)

# extract most general category
category = function(x) gsub("\\..*","",substring(x, 9, nchar(x)))
apply(as.data.frame(categories_map[,2]), 1, category) -> categories_map_general
head(categories_map_general)

# create key for most general category
data.frame(categories_map[,1], categories_map_general) -> key
c("article", "category") -> colnames(key) 
head(key)

####################################
# Step 3: Map articles to categories
####################################

# unfinished paths
map_unfin = function(y) lapply(1:length(split_articles_unfin[[y]][[1]]), 
            function(x) key[which(key[,"article"]==split_articles_unfin[[y]][[1]][x]),"category"])
lapply(1:length(split_articles_unfin), map_unfin) -> mapped_unfin
head(mapped_unfin)

# finished paths
map_fin = function(y) lapply(1:length(split_articles_fin[[y]][[1]]), 
                               function(x) key[which(key[,"article"]==split_articles_fin[[y]][[1]][x]),"category"])
lapply(1:length(split_articles_fin), map_fin) -> mapped_fin
head(mapped_fin)

# unfinished paths - source
map_source_unfin = function(x) mapped_unfin[[x]][1]
sapply(1:length(mapped_unfin), map_source_unfin) -> source_unfin
head(source_unfin)

# unfinished paths - N/A target

# finished paths - source
map_source_fin = function(x) mapped_fin[[x]][1]
sapply(1:length(mapped_fin), map_source_fin) -> source_fin
head(source_fin)

# finished paths - target
map_target_fin = function(x) mapped_fin[[x]][length(mapped_fin[[x]])]
sapply(1:length(mapped_fin), map_target_fin) -> target_fin
head(target_fin)

####################################
# Step 4: Prepare for plotting
####################################

# make the lists into data frames
as.data.frame(unlist(mapped_unfin)) -> mapped_unfin_df
as.data.frame(unlist(mapped_fin)) -> mapped_fin_df
as.data.frame(unlist(source_unfin)) -> source_unfin_df
as.data.frame(unlist(source_fin)) -> source_fin_df
as.data.frame(unlist(target_fin)) -> target_fin_df

# legend for numbers in the data frames
1:15 -> number
sort(unique(key$category)) -> name
data.frame(number, name) -> number_to_name
number_to_name

# count: unfinished paths
cbind(count(mapped_unfin_df, unlist(mapped_unfin)), number_to_name$name) -> counted_unfin
colnames(counted_unfin) = c("number", "count", "name")
arrange(counted_unfin, desc(count)) -> sorted_unfin
sorted_unfin

# count: finished paths
cbind(count(mapped_fin_df, unlist(mapped_fin)), number_to_name$name) -> counted_fin
colnames(counted_fin) = c("number", "count", "name")
arrange(counted_fin, desc(count)) -> sorted_fin
sorted_fin

# count: unfinished paths - source
cbind(count(source_unfin_df, unlist(source_unfin)), number_to_name$name) -> counted_source_unfin
colnames(counted_source_unfin) = c("number", "count", "name")
arrange(counted_source_unfin, desc(count)) -> sorted_source_unfin
sorted_source_unfin

# count: finished paths - source
cbind(count(source_fin_df, unlist(source_fin)), number_to_name$name) -> counted_source_fin
colnames(counted_source_fin) = c("number_source", "count_source", "name_source")

# count: finished paths - target
cbind(count(target_fin_df, unlist(target_fin)), number_to_name$name) -> counted_target_fin
colnames(counted_target_fin) = c("number_target", "count_target", "name_target")

# combine: finished paths - source and target
cbind(counted_source_fin, counted_target_fin) -> combined
transmute(combined, number = number_source, name = name_source, total = count_source + count_target) -> counted_combined
arrange(counted_combined, desc(total)) -> sorted_source_target_fin
sorted_source_target_fin

####################################
# Step 5: Plot counts by category
####################################

# unfinished paths 
ggplot(sorted_unfin, aes(x = reorder(name, count), y = count)) +
  geom_col() +
  coord_flip() +
  labs(x = "Category", y = "Count", title = "Unfinished Paths by Category")

ggplot(sorted_unfin, aes(x = reorder(name, count), y = count)) +
  geom_point() +
  coord_flip() +
  scale_y_continuous(trans = 'log10') +
  labs(x = "Category", y = "Count", title = "Unfinished Paths by Category")

# finished paths
ggplot(sorted_fin, aes(x = reorder(name, count), y = count)) +
  geom_col() +
  coord_flip() +
  labs(x = "Category", y = "Count", title = "Finished Paths by Category")

ggplot(sorted_fin, aes(x = reorder(name, count), y = count)) +
  geom_point() +
  coord_flip() +
  scale_y_continuous(trans = 'log10') +
  labs(x = "Category", y = "Count", title = "Finished Paths by Category")

# unfinished paths - source
ggplot(sorted_source_unfin, aes(x = reorder(name, count), y = count)) +
  geom_col() +
  coord_flip() +
  labs(x = "Category", y = "Count", title = "Unfinished Path Sources by Category")

ggplot(sorted_source_unfin, aes(x = reorder(name, count), y = count)) +
  geom_point() +
  coord_flip() +
  scale_y_continuous(trans = 'log10') +
  labs(x = "Category", y = "Count", title = "Unfinished Path Sources by Category")

# finished paths - source and target
ggplot(sorted_source_target_fin, aes(x = reorder(name, total), y = total)) +
  geom_col() +
  coord_flip() +
  labs(x = "Category", y = "Count", title = "Finished Path Sources and Targets by Category")

ggplot(sorted_source_target_fin, aes(x = reorder(name, total), y = total)) +
  geom_point() +
  coord_flip() +
  scale_y_continuous(trans = 'log10') +
  labs(x = "Category", y = "Count", title = "Finished Path Sources and Targets by Category")



