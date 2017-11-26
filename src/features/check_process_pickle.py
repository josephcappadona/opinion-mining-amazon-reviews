from collections import defaultdict
import pickle
import sys

if len(sys.argv) < 1:
  print("Specify pickle filepath.")
  exit()

def dd():
  return [defaultdict(list), 0]

with open(sys.argv[1], 'rb') as file:
  reviews = pickle.load(file)
  for asin, (feature_modifier_list, count) in reviews.iteritems():
    print "ASIN: {}, # reviews: {}".format(asin, count) 
    for phrase, adjs in feature_modifier_list:
      print "{} ({}), {}".format(phrase, len(adjs), adjs)
