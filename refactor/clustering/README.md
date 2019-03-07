
### Example
```
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz | gunzip > musical_instruments_reviews.json

python preprocess_corpus.py musical_instruments_reviews.json musical_instruments_corpus.txt
python build_clusters.py musical_instruments_corpus.txt musical_instruments_classes.txt w2v_sample_config.yaml
```

### Output
```
with open('musical_instruments_classes.txt', 'rt') as f:
    for line in f:
        word, class_id = line.split()
        print(word, class_id)
```
