from collections import defaultdict
import pickle
import sys

if len(sys.argv) < 1:
  print("Specify pickle filepath.")
  exit()

total_count = 0

with open(sys.argv[1], 'rb') as file:
  products = pickle.load(file)
  for asin, (feature_modifier_list, count) in products.iteritems():
    total_count += count
    print "ASIN: {}, # reviews: {}".format(asin, count) 
    for phrase, adjs in feature_modifier_list:
      print "{} ({}), {}".format(phrase, len(adjs), adjs)

print "# products: {0}, # reviews: {1}".format(len(products), total_count)
