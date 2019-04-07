
### Usage
```
sh install_corenlp.sh

cp ../word2vec/electronics_servers_reviews.json .

java -mx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
python test.py electronics_servers_reviews.json
```

### Details

`lexicon.txt` contains the base opinion word lexicon. Lines 1, 2, and 3 contain positive, negative, and neutral opinion words, respectively.

`corpus.py` provides a data structure for extracting and keeping track of dependency information that CoreNLP extracts from the corpus.

`double_prop.py` provides an implementation of the double propagation algorithm and the data structures necessary to store the associated information for further processing and analysis.

`extract.py` combines `corpus.py` and `double_prop.py` into a single script that extracts dependency information from the corpus and subsequently runs the double propagation algorithm until no new feature or opinion words are found.

`test.py` takes in review data, extracts the dependency information, and runs one iteration of double propagation. This serves to simply demonstrate sample output of the double propagation algorithm.
