import sys
import gzip
import json

if len(sys.argv) < 2:
    print('Usage:  python metadata.py ASIN_1 [ASIN_2, ...]')
    quit()

FILENAME = 'meta_Electronics.json.gz'
ASINS = sys.argv[1:]
METADATA_COLUMNS = ['id', 'title', 'categories', 'description', 'image_url']

def get_metadata_lines():
    with gzip.open(FILENAME, 'r') as f:
        for line in f:
            yield eval(line)

def get_metadata_lines_subset(asins):
    count = 0
    with gzip.open(FILENAME, 'r') as f:
        for line in f:
            count += 1
            if count % 100000 == 0: print(count)
            for asin in ASINS:
                if asin in str(line):
                    yield eval(line)

print("Retrieving metadata...")
lines = get_metadata_lines_subset(ASINS)
asin_metadatas = list(lines)
subset_asin_metadatas = [x for x in asin_metadatas if x['asin'] in ASINS]

print("\nFormatting metadata for data store...\n")
d = {x['asin']: x for x in subset_asin_metadatas}
asins = list(d.keys())
for asin in asins:
    # reformat certain fields
    d[asin]['image_url'] = d[asin]['imUrl']
    d[asin]['id'] = d[asin]['asin']
    d[asin]['categories'] = ','.join(d[asin]['categories'][0]) + ','
    if len(d[asin]['description']) > 255:
        d[asin]['description'] = d[asin]['description'][:255]

    # remove unneeded data
    keys = list(d[asin].keys())
    for key in keys:
        if key not in METADATA_COLUMNS:
            del d[asin][key]

from pprint import pprint
pprint(d)
outfile = 'asin_subset_metadata_1.json'
f = open(outfile, 'wt')
json.dump(list(d.values()), f)
f.close()
print('Metadata saved to {}\n'.format(outfile))

