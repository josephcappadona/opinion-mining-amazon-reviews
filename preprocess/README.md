
### Usage

```
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Electronics.json.gz | gunzip > electronics_metadata.json
wget -O - http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Electronics_5.json.gz | gunzip > electronics_reviews.json

python preprocess_metadata.py electronics_metadata.json electronics_categories.pkl > electronics_categories.txt
python filter_reviews.py electronics_reviews.json electronics_categories.pkl "Servers" electronics_servers_reviews.json
```

### Data Format
```
with open('electronics_metadata.json', 'rt') as f:
    for line in f:
        product_json = json.loads(line)

        asin = product_json['asin']
        title = product_json['title']
        categories = product_json['categories'][0]
        description = product_json['description']
        img_url = product_json['imUrl']
        price = product_json['price'] if 'price' in product_json else None
        sales_rank = product_json['salesRank'] if 'salesRank' in product_json else None
        related = product_json['related'] if 'related' in product_json else None

        print(asin, title, categories, description, img_url, price, sales_rank, related)


with open('electronics_servers_reviews.json', 'rt') as f:
    for line in f:
        review_json = json.loads(line)

        asin = review_json['asin']
        rating = review_json['overall']
        review_text = review_json['reviewText']

        print(asin, rating, review_text)
```
