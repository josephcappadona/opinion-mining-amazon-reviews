"""
Initial dependency parsing attempt.

Sumit/Joe (10/9): miscategorized some parts of speech, try using stanford core NLP
"""
import sys
import time
import spacy # download models w "python -m spacy.en.download all"
import json
import pickle
from pprint import pprint
from collections import defaultdict
from nltk import Tree
from spacy.symbols import nsubj, VERB

if len(sys.argv) < 3:
  raise ValueError

MAX_ = 300  # set to number of reviews you want to process (for short tests)
filepath = sys.argv[1]  # path to review data
filename = filepath.split('/')[-1]
OUTPUT_DIR = sys.argv[2]  # path to output directory


en_nlp = spacy.load('en')

print ("Opening file {}".format(filepath))

file_ = open(filepath, 'r')

noun_map = defaultdict(int)
adj_map = defaultdict(int)
adv_map = defaultdict(int)
very_map = defaultdict(int)
all_map = defaultdict(int)
review_jsons = []
i = 0
print ("Processing file {}\n".format(filepath))
for line in file_:
  review_json = json.loads(line)
  review_jsons += review_json
  
  b = False
  i += 1
  if i > MAX_:
    break
  if i % 100 == 0:
    print ("Processing review {}".format(i))
  
  doc = en_nlp(review_json['reviewText'])
  for element in doc:
    word = element.text
    pos = element.pos_
    all_map[(word, pos)] += 1
    if pos == "NOUN":
      noun_map[word] += 1
    elif pos == "ADJ":
      adj_map[word] += 1
    elif pos == "ADV":
      adv_map[word] += 1

pprint(sorted(all_map.items(), key=lambda e:e[1]))
output_file = OUTPUT_DIR + "/{}_{}.pickle".format(filename, str(int(time.time())))
with open(output_file, 'w+') as outfile:
  pickle.dump(all_map, outfile, protocol=pickle.HIGHEST_PROTOCOL)

file_.close()

'''
doc = en_nlp(review['reviewText'])

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_


[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

print (review['reviewText'])

print([(w.text, w.pos_) for w in doc])
'''

