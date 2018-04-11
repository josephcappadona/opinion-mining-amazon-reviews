import glob
import json
from collections import OrderedDict
from sys import argv

if len(argv) < 3:
    print('Usage:  python combine_product_qualities.py PATH/TO/PQ/DIR/ MAX [ASIN_1 ASIN_2 ...]')
    quit()

dir_ = argv[1]
pq_path = dir_ + '/*'
pq_filenames = glob.glob(pq_path)
valid_asins = set(argv[3:] if len(argv) > 3 else [fn.split('/')[-1].split('.')[0] for fn in pq_filenames if 'PQs_combined' not in fn.split('/')[-1]])

MAX = int(argv[2])

# keys that correspond to their order in the data store
ORDERED_PQ_KEYS = ['id', 'product', 'quality_class', 'quality_list_json', 'primary_quality', 'num_positive', 'num_negative']

combined = []
for filename in pq_filenames:
    if 'PQs_combined' not in filename.split('/')[-1]:
        print('Processing {}'.format(filename))
        datafile = open(filename)
        data = datafile.readlines()[0]
        pq_list = eval(data)

        new_pq_list = [] # list for filtered/modified product quality data
        for json_ in pq_list:
            # clean data
            if json_['product'] not in valid_asins:
                continue
            if 'quality' in json_:
                json_['primary_quality'] = json_['quality']
                json_.pop('quality', None)
            if 'cluster_num_positive' in json_ and 'cluster_num_negative' in json_:
                json_['num_positive'] = json_['cluster_num_positive']
                json_['num_negative'] = json_['cluster_num_negative']

            # place only keys present in data store into an ordered dict
            new_json = OrderedDict()
            for key in ORDERED_PQ_KEYS:
                new_json[key] = json_[key]
            new_pq_list.append(new_json)

        new_pq_list_sorted = sorted(new_pq_list, reverse=True, key=lambda pq: pq['num_positive']+pq['num_negative'])
        combined.extend(new_pq_list_sorted[:MAX])
        print('Added {} product qualities\n'.format(len(new_pq_list_sorted[:MAX])))

OUTFILE_NAME = 'PQs_combined_{}_{}.json'.format(len(combined), MAX)
OUTFILE_PATH = dir_ + '/' + OUTFILE_NAME
print('Writing {} combined product qualities (over {} products) to {}'.format(len(combined), len(valid_asins), OUTFILE_PATH))

json.dump(combined, open(OUTFILE_PATH, 'w'))

