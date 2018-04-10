import glob
import json
from collections import OrderedDict
from sys import argv

if len(argv) != 2:
    print('Usage:  python combine_product_qualities.py PATH/TO/PQ/DIR/')
    quit()

ORDERED_PQ_KEYS = ['id', 'product', 'quality_class', 'quality_list_json', 'primary_quality', 'num_positive', 'num_negative']

dir_ = argv[1]
path = dir_ + '/*'
onlyfiles = glob.glob(path)

combined = []
for filename in onlyfiles:
    if filename.split('.')[-1] == 'json' and filename.split('/')[-1] != 'combined.json':
        print('Processing {}'.format(filename))
        datafile = open(filename)
        data = datafile.readlines()[0]
        pq_list = eval(data)

        new_pq_list = [] # list for filtered/modified product quality data
        for json_ in pq_list:
            # clean data
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

        combined.extend(new_pq_list)
        print('Added {} product qualities\n'.format(len(new_snippet_list)))

OUTFILE = 'PQs_combined.json'
print('Writing combined product qualities json to {}'.format(OUTFILE))
json.dump(combined, open(OUTFILE, 'w'))

