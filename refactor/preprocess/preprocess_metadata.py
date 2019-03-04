from sys import argv as args
from collections import defaultdict
import pickle


def get_metadata(metadata_filepath):
    print('Fetching metadata from \'%s\'...' % metadata_filepath)
    with open(metadata_filepath, 'rt') as metadata_file:
        for line in metadata_file:
            yield eval(line)

def build_product_categories(metadata):
    print('Building product categories...')
    category_to_products = defaultdict(list)
    for product in metadata:
        for category in product['categories'][0]:
            category_to_products[category].append(product)
    return category_to_products

def save_product_categories(category_metadata, output_filepath):
    print('Saving product category metadata to \'%s\'' % output_filepath)
    with open(output_filepath, 'w+b') as category_metadata_file:
        pickle.dump(category_metadata, category_metadata_file)

if __name__ == '__main__':

    if len(args) != 3:
        print('USAGE:  preprocess_metadata.py METADATA.json CATEGORY_METADATA_OUTPUT.pkl')
        exit()
    metadata_filepath = args[1]
    category_metadata_output_filepath = args[2]

    metadata = get_metadata(metadata_filepath)
    product_categories = build_product_categories(metadata)
    save_product_categories(product_categories, category_metadata_output_filepath)

    print('\nCategories:')
    for category in product_categories:
        print('\t"%s"' % category)
