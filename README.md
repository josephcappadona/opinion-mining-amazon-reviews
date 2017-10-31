# Aggregating Insights from Amazon Product Reviews
## Senior Design 2017-18, University of Pennsylvania
Team: Raymond Yin, Carolina Zheng, Sumit Shyamsukha, Joe Cappadona

Advisor: Prof. Chris Callison-Burch

# What is this?
Online shoppers value reviewer opinions, but typically only read a few reviews. Reviews are a one-dimensional rating of a product, which is composed of individual attributes that may be more or less important to each shopper.

We are building a webapp that aggregates Amazon review opinions about a product’s individual attributes to help potential customers make more informed purchasing decisions.

# Goals
1. Build a topical model that determines product attributes that are important to reviewers for each product category.
2. Build a classifier that predicts the sentiment for each product attribute given the reviews for an individual product.
3. Create a webapp that online shoppers can use to obtain product insights drawn from our models.

# Documents and Presentations
[Prospectus](https://docs.google.com/document/d/1361A_TWmM_9vMqyUZn54dAXiFLXCjP1nHvMBFuujl08/)

[Proposal Review Presentation, 10/12](https://docs.google.com/presentation/d/1Mk74AG5LYhIhdV7RcbA-OsCsA1ILOk9LSzZt8JfhTtg/)

[Lightning Talk, 10/19](https://docs.google.com/document/d/1VA6_tRsiSYoE_d5CvkZ4U52NRldFUp5Mq_QTt4HwOsw/)

# Local Directory Setup
1. Create dir `../data/` and place review data within
2. Create dir `../output/` qsub script output
3. Create dir `../results/` corenlp.py processing output
4. Create dir `../virtualenv/` and instantiate with `./requirements.txt`
5. Create dir `../CoreNLP/` and place CoreNLP jars within

# How to Use
1. Run `qsub dispath_corenlp.sh` from nlpgrid head node
2. Find output in pickle format, one review per line, in `../results/` labeled with timestamp (YYYY-MM-DD\_HH-MM-SS
