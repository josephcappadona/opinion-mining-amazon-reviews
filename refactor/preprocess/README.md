
### Example

```
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz | gunzip > electronics_metadata.json
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz | gunzip > electronics_reviews.json

python preprocess_metadata.py electronics_metadata.json electronics_categories.pkl
python filter_reviews.py electronics_reviews.json electronics_categories.pkl "Servers" electronics_servers_reviews.json
```

