
### Example
```
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz | gunzip > musical_instruments_reviews.json

python preprocess_corpus.py musical_instruments_reviews.json musical_instruments_corpus.txt
python build_classes.py ../../../word2vec/word2vec musical_instruments_corpus.txt musical_instruments_classes.txt w2v_sample_config.yaml
```

### Sample Output
```
with open('musical_instruments_reviews.json') as f:
    for line in f:
        review_json = json.loads(line)

        asin = review_json['asin']
        rating = review_json['overall']
        review_text = review_json['reviewText']
        print(asin, rating, review_text)

with open('musical_instruments_classes.txt', 'rt') as f:
    for line in f:
        word, class_id = line.split()
        print(word, class_id)

with open('musical_instruments_corpus.txt', 'rt') as f:
    for line in f:
        sentence = line.strip()
        print(sentence)
```
