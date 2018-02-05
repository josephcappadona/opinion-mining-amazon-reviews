import yaml
import json
import pickle
import sys
import time
from collections import Counter

if len(sys.argv) == 2:
	NUM_REVIEWS = int(sys.argv[1])
else:
	NUM_REVIEWS = sys.maxint

config = yaml.load(open("../config.yml"))
review_file = open("../" + config["full_electronics_path"], "r")
review_freq_buckets = {"1-20": [], "21-50": [], "51-100": [], "101-1000": [], "1001+": []}
asin_dict = Counter()
i = 0
start_time = time.time()

for line in review_file:
	review = json.loads(line)
	asin_dict[review["asin"]] += 1
	i += 1
	if (i >= NUM_REVIEWS):
		break
	
review_file.close()
for asin, freq in asin_dict.items():
	if freq <= 20:
		review_freq_buckets["1-20"].append(asin)
	elif freq <= 50:
		review_freq_buckets["21-50"].append(asin)
	elif freq <= 100:
		review_freq_buckets["51-100"].append(asin)
	elif freq <= 1000:
		review_freq_buckets["101-1000"].append(asin)
	else:
		review_freq_buckets["1001+"].append(asin)

for bucket, asin_list in review_freq_buckets.items():
	print("{} reviews: {}".format(bucket, len(asin_list)))

output_path = "../../../results/top_products.pkl"
with open(output_path, "w+") as output_file:
	pickle.dump(review_freq_buckets, output_file, -1)

time_elapsed = time.time() - start_time
print("Time elapsed (s): {}".format(time_elapsed))
