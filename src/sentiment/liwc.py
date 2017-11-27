"""Extract sentiment from liwc dictionary.

The LIWC2015 dictionary attaches each prefix to a category.
See categories here:
https://github.com/sosolimited/semantic_sabotage/wiki/LIWC-Categories


"""

import csv
import re
import time

# FILEPATH = '../../lib/liwc_2015.csv'

FILEPATH = '../lib/liwc_2015.csv'


POSITIVE = 'POSEMO'
NEGATIVE = 'NEGEMO'

VALENCE_CATEGORIES = [POSITIVE, NEGATIVE]


def _is_wildcard(prefix):
    return prefix[-1] == '*'


def _build_liwc_dictionary():
    start = time.time()
    print('Building LIWC dictionary:'),
    CATEGORY_OF_REGEX = {}
    CATEGORY_OF_WORD = {}

    with open(FILEPATH) as f:
        reader = csv.reader(f)
        for prefix, category in reader:
            _store_regex(prefix, category, CATEGORY_OF_REGEX, CATEGORY_OF_WORD)

    print('Finished in %s seconds' % (time.time() - start))
    return (CATEGORY_OF_REGEX, CATEGORY_OF_WORD)


def _store_regex(prefix, category, category_of_regex, category_of_word):
    if category in VALENCE_CATEGORIES:
        if _is_wildcard(prefix):
            regex = re.compile(prefix[:-1])
            category_of_regex[regex] = category
        else:
            category_of_word[prefix] = category


def _get_category(word, category_of_regex, category_of_word):
    # If word is directly listed in LIWC dictionary, return category
    category = category_of_word.get(word)
    if category:
        return category

    # If word matches prefix listed in LIWC dictionary, return category
    for regex, category in category_of_regex.items():
        if regex.match(word):
            return category

def get_valence(word, category_dicts=_build_liwc_dictionary()):
    category = _get_category(word, *category_dicts)
    if category in VALENCE_CATEGORIES:
        return category

