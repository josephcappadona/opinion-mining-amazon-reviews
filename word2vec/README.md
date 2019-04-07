
### Usage
```
sh install_word2vec.sh

cp ../preprocess/electronics_servers_reviews.json .

python preprocess_corpus.py electronics_servers_reviews.json electronics_servers_corpus.txt
python build_classes.py word2vec/word2vec electronics_servers_corpus.txt electronics_servers_classes.txt w2v_sample_config.yaml
```

### Details

`preprocess_corpus.py` takes in reviews from a single category and creates a corpus document that contains all of the sentences from all of the reviews with one sentence per line.

`build_classes.py` runs this corpus through word2vec and produces a text file with each line containing a word in the corpus and its class id.

`postprocess_classes.py` provides a method to take the class information output by `build_classes.py` and compile it into data structures that can be easily queried to find the class id of a given word or a list of all the words in a particular class.

### Data Format
```
with open('electronics_servers_classes.txt', 'rt') as f:
    for line in f:
        word, class_id = line.split()
        print(word, class_id)

with open('electronics_servers_corpus.txt', 'rt') as f:
    for line in f:
        sentence = line.strip()
        print(sentence)
```
