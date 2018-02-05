from collections import defaultdict
import pickle
import time
import sys
import json
from nltk.parse.corenlp import CoreNLPDependencyParser
from datetime import datetime

if len(sys.argv) < 5:
  print "Usage: python corenlp_sandbox.py review_data_path output_dir max [skip]"
  exit()

filepath = sys.argv[1]  # path to review data
filename = filepath.split('/')[-1]
OUTPUT_DIR = sys.argv[2]  # path to output directory
MAX_ = int(sys.argv[3])  # number of reviews you want to process (for short tests)
START_AFTER = int(sys.argv[4]) if len(sys.argv) >= 5 else 0

nlp = CoreNLPDependencyParser(url='http://localhost:9000')

review_file = open(filepath, 'r')
_ = [review_file.readline() for _ in range(START_AFTER)]
reviews = [review_file.readline() for _ in range(MAX_)]

reviews_processed = []
start_time = time.time()
sys.stderr.write("Parsing\n")

def parse_review(text):
    parse = nlp.parse_text(text)
    phrase_modifier_dict = defaultdict(list) # nn phrase -> adv + adj
    for sentence in parse:
        phrase_dict = defaultdict() # nn -> nn phrase
        modifier_dict = defaultdict() # nn -> adj
        adv_dict = defaultdict() # nn -> adv + adj
        negated_adjs = set()
        for (gov, gov_pos), dependency, (dep, dep_pos) in sentence.triples():
            if not gov.isalpha() or not dep.isalpha():
                continue
            gov = gov.lower()
            dep = dep.lower()
            if dependency == 'nsubj' and dep_pos == 'NN':
                modifier_dict[dep] = gov
            elif dependency == 'amod' and gov_pos == 'NN':
                modifier_dict[gov] = dep
            elif dependency == 'compound':
                phrase_dict[gov] = dep + ' ' + gov
            elif dependency == 'neg':
                negated_adjs.add(gov) 
            #elif dependency == 'advmod':
                #adv_dict[gov] = dep + ' ' + gov
        for noun, adj in modifier_dict.items():
            if noun in phrase_dict:
                noun = phrase_dict[noun]
            if adj in negated_adjs:
                adj = "*" + adj
            #if adj in adv_dict:
                #adj = adv_dict[adj]
            phrase_modifier_dict[noun].append(adj)
    return phrase_modifier_dict

for review in reviews:
  review_json = json.loads(review)
  try:
    phrase_modifier_dict = parse_review(review_json['reviewText'])
  except ValueError:
    sys.stderr.write("Failed to parse review with text: " + review_json['reviewText'])
    phrase_modifier_dict = {}
  reviews_processed.append((review_json['asin'], phrase_modifier_dict))
  print "\n\n{} {}\n------------------".format(review_json['reviewerID'], review_json['asin'])

review_file.close()
sys.stderr.write("Finished parsing\n")

outfilename = "{}_{}_{:%Y-%m-%d_%H-%M-%S}.pickle".format(sys.argv[0].split('/')[0], filename, datetime.now())
outfilepath = OUTPUT_DIR + "/" + outfilename
with open(outfilepath, 'w+') as outfile:
  pickle.dump(reviews_processed, outfile, -1)

time_elapsed = time.time() - start_time
print "Time elapsed (s): {}".format(time_elapsed)
print "\tApprox {}s per review".format(time_elapsed/len(reviews_processed))
sys.stderr.write("Pickled\n")
