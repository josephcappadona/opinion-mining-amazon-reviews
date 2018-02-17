import yaml
import json
import pickle
import sys
import time

if len(sys.argv) == 2:
	NUM_REVIEWS = int(sys.argv[1])
else:
	NUM_REVIEWS = sys.maxint

config = yaml.load(open("../config.yml"))
review_file = open("../../data/reviews_Electronics.json", "r")
i = 0
start_time = time.time()

for line in review_file:
	review = json.loads(line)
	asin_dict[review["asin"]] += 1
	i += 1
	if (i >= NUM_REVIEWS):
		break

review_file.close()

time_elapsed = time.time() - start_time
print("Time elapsed (s): {}".format(time_elapsed))
