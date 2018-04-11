import glob
import json
from collections import OrderedDict
from sys import argv
from pprint import pprint

if len(argv) < 3:
    print('Usage:  python combine_snippets.py PATH/TO/SNIPPETS/DIR/ MAX [ASIN_1 ASIN_2 ...]\n\tMAX = maximum number of snippets for a particular product')
    quit()

dir_ = argv[1]
snippet_path = dir_ + '/*'
snippet_filenames = glob.glob(snippet_path)

valid_asins = set(argv[3:] if len(argv) > 3 else [fn.split('/')[-1].split('.')[0] for fn in snippet_filenames if 'snippets_combined' not in fn.split('/')[-1]])

MAX = int(argv[2])

# keys that correspond to their order in the data store
ORDERED_SNIPPET_KEYS = ['id', 'product', 'quality_class', 'quality', 'polarity', 'sentence', 'helpful_count']


# for backfilling quality_class_id
import pickle
CLASS_PICKLE = "../src/clustering/results/clean-classes.pkl"
feature_to_class = pickle.load(open(CLASS_PICKLE, "rb"))


combined = []
for filename in snippet_filenames:
    if 'snippets_combined' not in filename.split('/')[-1]:
        print('Processing {}'.format(filename))
        datafile = open(filename)
        data = datafile.readlines()[0]
        snippet_list = eval(data)

        new_snippet_list = [] # list for filtered/modified snippet data
        for json_ in snippet_list:
            # clean data
            if json_['asin'] not in valid_asins:
                continue
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

        new_snippet_list_sorted = sorted(new_snippet_list, reverse=True, key=lambda s: s['helpful_count'])
        combined.extend(new_snippet_list_sorted[:MAX])
        print('Added {} snippets\n'.format(len(new_snippet_list_sorted[:MAX])))

OUTFILE_NAME = 'snippets_combined_{}_{}.json'.format(len(combined), MAX)
OUTFILE_PATH = dir_ + '/' + OUTFILE_NAME
print('Writing {} combined snippets (over {} products) to {}'.format(len(combined), len(valid_asins), OUTFILE_PATH))

json.dump(combined, open(OUTFILE_PATH, 'w'))

