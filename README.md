## Steps

### 1. Preprocess

Downloads reviews and review metadata. Review metadata contains information on the products and subcategories in a given category heading. For example, the "Electronics" category contains the subcategories "Computers & Accessories", "Speakers", "Headphones", etc.

`preprocess_metadata.py` aggregates the metadata information into a data structure that allows one to easily find all products in a given subcategory (i.e., it forms a dictionary from category name to category products).

`filter_reviews.py` takes in all of the reviews for a category and outputs a file with only the reviews for a specified subcategory. For example, it will take in all Electronics reviews and output only those that fall in the "Headphones" subcategory.


### 2. Word2Vec

Downloads and builds Google's [word2vec](https://code.google.com/archive/p/word2vec/) library. Copies over filtered review data from Step 1 into the current directory. Creates a corpus of sentences based on this review data, and runs word2vec to transform the vocabulary from the corpus into vectors such that words that share similar contexts are located in close proximity in the vector space. Word2vec then clusters these word embeddings to creates "classes" of words (i.e., groups of words which have strong semantic and syntactic relations).

`preprocess_corpus.py` takes in reviews from a single category and creates a corpus document that contains all of the sentences from all of the reviews with one sentence per line.

`build_classes.py` runs this corpus through word2vec and produces a text file with each line containing a word in the corpus and its class id.

`postprocess_classes.py` provides a method to take the class information output by `build_classes.py` and compile it into data structures that can be easily queried to find the class id of a given word or a list of all the words in a particular class.


### 3. Double Propagation

Downloads [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) library. Copies filtered review data from Step 2 into the current directory. Starts up CoreNLP server locally. Runs Qiu, et al.'s [double propagation algorithm](https://dl.acm.org/citation.cfm?id=1970422) to discover product features by bootstrapping off of a base opinion word lexicon of known opinion words (e.g., good, bad, green).

`lexicon.txt` contains the base opinion word lexicon. Lines 1, 2, and 3 contain positive, negative, and neutral opinion words, respectively.

`corpus.py` provides a data structure for extracting and keeping track of dependency information that CoreNLP extracts from the corpus.

`double_prop.py` provides an implementation of the double propagation algorithm and the data structures necessary to store the associated information for further processing and analysis.

`extract.py` combines `corpus.py` and `double_prop.py` into a single script that extracts dependency information from the corpus and subsequently runs the double propagation algorithm until no new feature or opinion words are found.

`test.py` takes in review data, extracts the dependency information, and runs one iteration of double propagation. This serves to simply demonstrate sample output of the double propagation algorithm.


## TODOs

* Compile double propagation output into tables + graphics for analysis

* Build functions to look at correlation between opinion word sentiment and the propability that the word occurs in a positive review vs negative review, possibly use this information (or VADER information) in lieu of how sentiment is propgated in the NN->JJ case (Intra-review Rule)

* change example category to one with smaller files
