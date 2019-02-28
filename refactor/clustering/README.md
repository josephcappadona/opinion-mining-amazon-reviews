### Example
```
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz | gunzip > MI_reviews.json
python preprocess_corpus.py MI_reviews.json MI_corpus.txt
python build_clusters.py MI_corpus.txt MI_clusters.txt w2v_MI_config.yaml
```
