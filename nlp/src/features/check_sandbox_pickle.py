import pickle
import sys

if len(sys.argv) < 1:
  print("Specify pickle filepath.")
  exit()

with open(sys.argv[1], 'rb') as file:
  reviews = pickle.load(file)
  for review_asin, phrase_modifier_dict in reviews:
    print "ASIN: {}".format(review_asin) 
    for phrase, modifier in phrase_modifier_dict.items():
      print((phrase, modifier))

print("# reviews processed: {0}".format(len(reviews)))
