from sys import argv as args
from collections import defaultdict
import pickle
import json

def get_reviews(reviews_filepath):
    print('Fetching reviews from \'%s\'...' % reviews_filepath)
    with open(reviews_filepath, 'rt') as reviews_file:
        for line in reviews_file:
            yield eval(line)

def get_category_metadata(category_metadata_filepath):
    print('Loading category metadata from \'%s\'...' % category_metadata_filepath)
    with open(category_metadata_filepath, 'rb') as category_metadata_file:
        return pickle.load(category_metadata_file)

def get_asins(category, category_metadata):
    print('Aggregating ASINs for category \'%s\'...' % category)
    return [product['asin'] for product in category_metadata[category]]

def filter_reviews(reviews, asins):
    print('Filtering reviews for ASINs \'%s\'...' % asins)
    filtered_reviews = []
    asins = set(asins)
    for review in reviews:
        asin = review['asin']
        if asin in asins:
            filtered_reviews.append(review)
    return filtered_reviews

def json_dump_reviews(reviews, output_filepath):
    print('Dumping %d reviews to \'%s\'...' % (len(reviews), output_filepath))
    with open(output_filepath, 'w+t') as filtered_reviews_file:
        for review in reviews:
            filtered_reviews_file.write(json.dumps(review))

if __name__ == '__main__':

    if len(args) != 5:
        print('USAGE:  python filter_reviews.py REVIEWS.json CATEGORY_METADATA.pkl PRODUCT_CATEGORY FILTERED_REVIEWS_OUTPUT.json')
        exit()
    reviews_filepath = args[1]
    category_metadata_filepath = args[2]
    category = args[3]
    filtered_reviews_output_filepath = args[4]

    category_metadata = get_category_metadata(category_metadata_filepath)
    asins = get_asins(category, category_metadata)

    reviews = get_reviews(reviews_filepath)
    filtered_reviews = filter_reviews(reviews, asins)
    json_dump_reviews(filtered_reviews, filtered_reviews_output_filepath)

