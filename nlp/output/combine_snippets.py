import glob
import json
from collections import OrderedDict
from sys import argv
from pprint import pprint

if len(argv) != 2:
    print('Usage:  python combine_snippets.py PATH/TO/SNIPPETS/DIR/')
    quit()

dir_ = argv[1]
path = dir_ + '/*'
onlyfiles = glob.glob(path)

OUTFILE_NAME = 'snippets_combined.json'

# keys that correspond to their order in the data store
ORDERED_SNIPPET_KEYS = ['id', 'product', 'quality_class', 'quality', 'polarity', 'sentence', 'helpful_count']

# for backfilling quality_class_id
import pickle
CLASS_PICKLE = "../src/clustering/results/clean-classes.pkl"
feature_to_class = pickle.load(open(CLASS_PICKLE, "rb"))


combined = []
for filename in onlyfiles:
    if filename.split('.')[-1] == 'json' and filename.split('/')[-1] != OUTFILE_NAME:
        print('Processing {}'.format(filename))
        datafile = open(filename)
        data = datafile.readlines()[0]
        snippet_list = eval(data)

        new_snippet_list = [] # list for filtered/modified snippet data
        for json_ in snippet_list:
            # clean data
            json_['product'] = json_['asin']
            json_['id'] = ''
            if 'quality_class' not in json_:
                try:
                    json_['quality_class'] = feature_to_class[json_['quality']]
                    json_['helpful_count'] = json_['helpful_count']
                except KeyError:
                    continue

            # place only keys present in data store into an ordered dict
            new_json = OrderedDict()
            for key in ORDERED_SNIPPET_KEYS:
                new_json[key] = json_[key]
            new_snippet_list.append(new_json)

        combined.extend(new_snippet_list)
        print('Added {} snippets\n'.format(len(new_snippet_list)))

OUTFILE = dir_ + '/' + OUTFILE_NAME
print('Writing {} combined snippets json to {}'.format(len(combined), OUTFILE))
json.dump(combined, open(OUTFILE, 'w'))

