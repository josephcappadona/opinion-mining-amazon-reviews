
### Example
```
sh install_word2vec.sh

cp ../preprocess/electronics_servers_reviews.json .

python preprocess_corpus.py electronics_servers_reviews.json electronics_servers_corpus.txt
python build_classes.py word2vec/word2vec electronics_servers_corpus.txt electronics_servers_classes.txt w2v_sample_config.yaml
```

### Sample Output
```
with open('electronics_servers_reviews.json') as f:
    for line in f:
        review_json = json.loads(line)

        asin = review_json['asin']
        rating = review_json['overall']
        review_text = review_json['reviewText']
        print(asin, rating, review_text)

with open('electronics_servers_classes.txt', 'rt') as f:
    for line in f:
        word, class_id = line.split()
        print(word, class_id)

with open('electronics_servers_corpus.txt', 'rt') as f:
    for line in f:
        sentence = line.strip()
        print(sentence)
```
