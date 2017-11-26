from collections import defaultdict
import pickle
import sys

# Run within src/features directory
# Produces pickle with product asin -> ([(nn, [adjs])], # reviews)
if len(sys.argv) < 1:
  print("Specify filepath of the *file with a list of filenames* corresponding to output of corenlp_sandbox jobs.")
  exit()

THRESHOLD = 0.02 # % of all reviews that must mention this feature
product_features_dict_imt = defaultdict(lambda: [defaultdict(list), 0])
product_features_dict = dict()

with open(sys.argv[1], 'rb') as file:
  filepaths = file.readlines()
  filepaths = [x.strip() for x in filepaths] 

for fp in filepaths:
  with open(fp, 'rb') as file:
    print "Processing {}".format(fp)
    reviews = pickle.load(file) 
    for asin, review_dict in reviews:
      product_features_dict_imt[asin][1] += 1
      feature_dict = product_features_dict_imt[asin][0]
      for phrase, modifier in review_dict.iteritems():
        feature_dict[phrase].append(modifier)

print "Taking top and sorting"
for asin, (feature_dict, count) in product_features_dict_imt.iteritems():
  top_dict = {k: vs for k, vs in feature_dict.iteritems() if len(vs) * 1.0 / count >= THRESHOLD}
  sorted_top_list = sorted(top_dict.items(), key=lambda (k, vs): len(vs), reverse=True)
  product_features_dict[asin] = sorted_top_list, count

print "Pickling"
outfn = "features.pickle"
outfp = "./results" + "/" + outfn
with open(outfp, "w+") as outfile:
  pickle.dump(product_features_dict, outfile, -1)
