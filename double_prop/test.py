from sys import argv as args
from corpus import CorpusInfo
from double_prop import DoublePropagationInfo
import json

def get_reviews(reviews_filepath):
    with open(reviews_filepath, 'rt') as reviews_file:
        for line in reviews_file:
            yield json.loads(line)

if __name__ == '__main__':

    if len(args) != 2:
        print('USAGE:  python test.py REVIEWS.json')
        exit()
    reviews_filepath = args[1]

    reviews = [review['reviewText'] for review in get_reviews(reviews_filepath)]

    corpus_info = CorpusInfo(reviews)
    corpus_info.extract_dependency_information()
    dp = DoublePropagationInfo()
    print(list(dp.iterate(corpus_info)))

