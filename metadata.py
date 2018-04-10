import sys
import gzip
import json
import csv

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
            if count % 5000 == 0:
                print(count)
            for asin in ASINS:
                asin_str = "'asin': '{}'".format(asin)
                if asin_str in str(line):
                    yield eval(line)


def fill_in_default_fields(d):
    for field in METADATA_COLUMNS:
        d[field] = d.get(field) or ''


def export_to_csv(data):
    filename = 'asin_subset_metadata_1.csv'
    with open(filename, 'w') as csvfile:
        fieldnames = METADATA_COLUMNS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for v in data:
            writer.writerow(v)
    print('Metadata saved to {}\n'.format(filename))


def export_json(data):
    from pprint import pprint
    pprint(data)
    outfile = 'asin_subset_metadata_1.json'
    f = open(outfile, 'wt')
    json.dump(list(data), f)
    f.close()
    print('Metadata saved to {}\n'.format(outfile))


def format_metadata_dict(meta_dict):
    # Fill in default fields
    fill_in_default_fields(meta_dict)
    # reformat certain fields
    meta_dict['image_url'] = meta_dict['imUrl']
    meta_dict['id'] = meta_dict['asin']
    meta_dict['categories'] = ','.join(meta_dict['categories'][0]) + ','

    # Filter out columns originally not in there
    meta_dict = {k: v for k, v in meta_dict.items() if k in METADATA_COLUMNS}
    return meta_dict


print("Retrieving metadata...")
lines = get_metadata_lines_subset(ASINS)
print("\nFormatting metadata for data store...\n")
formatted_metadatas = (format_metadata_dict(metadata_dict)
                       for metadata_dict in lines)
export_json(formatted_metadatas)

# export_to_csv(formatted_metadatas)
