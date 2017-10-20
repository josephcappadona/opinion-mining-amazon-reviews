"""
Initial dependency parsing attempt.

Sumit/Joe (10/9): miscategorized some parts of speech, try using stanford core NLP
"""

import spacy
import json
import string
from pprint import pprint
from collections import defaultdict
from nltk import Tree

en_nlp = spacy.load('en')

filename = "reviews_Baby_5.json"
print ("Opening file {}".format(filename))

file = open(filename, 'r')
print ("Reading file {}".format(filename))
l = file.readlines()

noun_map = defaultdict(int)
adj_map = defaultdict(int)
adv_map = defaultdict(int)
very_map = defaultdict(int)
all_map = defaultdict(int)
review_jsons = [json.loads(review_str) for review_str in l]
i = -1
b = False
for review_json in review_jsons:
	i += 1
	if i % 100 == 0:
		print ("Processing review {}".format(i))
	doc = en_nlp(review_json['reviewText'])
	for w in doc:
		word = w.text
		pos = w.pos_
		if pos == "NOUN":
			noun_map[word] += 1
			all_map[(w.text, w.pos_)] += 1
		elif pos == "ADJ":
			adj_map[word] += 1
			all_map[(w.text, w.pos_)] += 1
		elif pos == "ADV":
			adv_map[word] += 1
			all_map[(w.text, w.pos_)] += 1
		if b == True:
			very_map[word] += 1
			b = False
		if word == "very":
			b = True
	if i == 3000:
		break

pprint(sorted(all_map.items(), key=lambda e:e[1]))
pprint(sorted(very_map.items(), key=lambda e:e[1]))
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