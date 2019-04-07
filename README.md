## Steps

### 1. Preprocess

Downloads reviews and review metadata. Review metadata contains information on the products and subcategories in a given category heading. For example, the "Electronics" category contains the subcategories "Computers & Accessories", "Speakers", "Headphones", etc.


### 2. Word2Vec

Downloads and builds Google's [word2vec](https://code.google.com/archive/p/word2vec/) library. Copies over filtered review data from Step 1 into the current directory. Creates a corpus of sentences based on this review data, and runs word2vec to transform the vocabulary from the corpus into vectors such that words that share similar contexts are located in close proximity in the vector space. Word2vec then clusters these word embeddings to creates "classes" of words (i.e., groups of words which have strong semantic and syntactic relations).


### 3. Double Propagation

Downloads [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) library. Copies filtered review data from Step 2 into the current directory. Starts up CoreNLP server locally. Runs Qiu, et al.'s [double propagation algorithm](https://dl.acm.org/citation.cfm?id=1970422) to discover product features by bootstrapping off of a base opinion word lexicon of known opinion words (e.g., good, bad, green).


## TODOs

* Compile double propagation output into tables + graphics for analysis

* Build functions to look at correlation between opinion word sentiment and the propability that the word occurs in a positive review vs negative review, possibly use this information (or VADER information) in lieu of how sentiment is propgated in the NN->JJ case (Intra-review Rule)

* change example category to one with smaller files
