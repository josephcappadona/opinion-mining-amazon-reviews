'''
Initial POS tagging and dependency parsing attempt using Stanford CoreNLP.

Joe (10/30): Pulls out some NN-JJ pairs effectively, but most opinion sentences are irregular
              and appear difficult to parse correctly. Doesn't handle contractions like "n't".
'''
from pprint import pprint
from nltk import ParentedTree, Tree
from collections import defaultdict
import json
import pickle
import sys
import time
import os
from datetime import datetime
from helper import traverse

# parse args
if len(sys.argv) < 5:
  print "Usage: python corenlp.py review_data_path output_dir max [skip]"
  exit()

filepath = sys.argv[1]  # path to review data
filename = filepath.split('/')[-1]
OUTPUT_DIR = sys.argv[2]  # path to output directory
MAX_ = int(sys.argv[3])  # number of reviews you want to process (for short tests)
START_AFTER = int(sys.argv[4]) if len(sys.argv) >= 5 else 0

from stanford_corenlp_pywrapper import CoreNLP
# for CoreNLP wrapper API, see https://github.com/brendano/stanford_corenlp_pywrapper
proc = CoreNLP("parse", corenlp_jars=["../../../CoreNLP/*"])

review_file = open(filepath, 'r')

_ = [review_file.readline() for _ in range(START_AFTER)]
reviews = [review_file.readline() for _ in range(MAX_)]

reviews_processed = []
start_time = time.time()
for review in reviews:
  review_json = json.loads(review)
  parse = proc.parse_doc(review_json['reviewText'])
  
  print "\n\n{} {}\n------------------".format(review_json['reviewerID'], review_json['asin'])

  results = []
  for sentence in parse['sentences']:
    sentence_parse = sentence['parse']
    tree = ParentedTree.fromstring(sentence_parse)
    tv = traverse(tree)
    tokens = sentence['tokens']
    deps = defaultdict(dict)
    deps_rev = defaultdict(dict)
    for dep,i,j in sentence['deps_cc']:
      if i not in deps:
        deps[i] = defaultdict(set)
      if j not in deps_rev:
        deps_rev[j] = defaultdict(set)
      deps[i][dep].add(j)
      deps_rev[j][dep].add(i)
    
    # glossary of dependencies: http://universaldependencies.org/en/dep/index.html
    # glossary of POS tags: https://stackoverflow.com/questions/1833252/java-stanford-nlp-part-of-speech-labels
    # also, for better intuition, play around with http://nlp.stanford.edu:8080/corenlp/process
    #    try sentences like "the sound quality is very poor and is not worth the price"
    nn_amods = defaultdict(list) # maps NN index to list of its children with amod dependency
    nn_compound_map = {}
    nn_np_map = defaultdict(list) # maps NN index to list of NP trees containing it
    nn_jj_map = defaultdict(list) # maps NN index to list of NP trees containing it
    nn_vp_map = defaultdict(list) # maps NN index to VP trees modifying it
    nsubjs = set() # set of tokens (indexes) receiving nsubj dependency
    jj_nsubj = defaultdict(list) # maps JJ index to corresponding nsubj index
    v_nsubj = defaultdict(list) # maps V index to corresponding nsubj index
    v_vp_map = {} # maps V index to tree of VP containing it
    jj_adjp_map = {} # maps JJ index to tree of ADJP containing it
    jj_vp_map = {} # maps JJ index to tree of VP containing it
    
    for index,pos_tag in enumerate(sentence['pos']):
      try:
        # traverse parse tree to leaf node
        leaf_node = next(tv)
      except StopIteration:
        break
      cur_node = leaf_node

      if pos_tag[:2] == "NN":
        if "amod" in deps[index]:
          nsubjs.add(index)
          nn_amods[index].extend(deps[index]["amod"])
          # TODO: get full ADJP for JJ ?
          while cur_node:
            # traverse tree backward to find full noun phrase containing this noun
            if cur_node.label() == "NP":
              nn_np_map[index].append(cur_node)
            cur_node = cur_node.parent()
        if "compound" in deps[index]:
          nn_compound_indexes = sorted(deps[index]["compound"].union([index]))
          nn_compound_map[index] = ' '.join([tokens[i] for i in nn_compound_indexes])
        
      if pos_tag[:2] == "JJ" or pos_tag[:2] == "NN":
        if "nsubj" in deps[index] and "cop" in deps[index]:
          subjs = deps[index]["nsubj"]
          jj_nsubj[index].extend(subjs)
          nsubjs.update(subjs)
          for subj in subjs:
            nn_jj_map[subj].append(index)
          if pos_tag[:2] == "NN":
            while cur_node and cur_node.label() != "NP":
              # traverse tree backward to find full adj phrase containing this adj (if it exists)
              cur_node = cur_node.parent()
            while cur_node and cur_node.parent() and cur_node.parent().label() == "NP":
              cur_node = cur_node.parent()
            np_node = cur_node
            jj_adjp_map[index] = np_node
          else:
            while cur_node and cur_node.label() != "ADJP":
              # traverse tree backward to find full adj phrase containing this adj (if it exists)
              cur_node = cur_node.parent()
            adjp_node = cur_node
            if adjp_node:
              jj_adjp_map[index] = adjp_node
            while cur_node and cur_node.label() != "VP":
            # traverse tree backward to find full verb phrase containing this verb (if it exists)
              cur_node = cur_node.parent()
            vp_node = cur_node
            if adjp_node and vp_node:
              jj_vp_map[index] = cur_node


      elif pos_tag[:1] == "V":
        if "nsubj" in deps[index]:
          subjs = deps[index]["nsubj"]
          v_nsubj[index].extend(subjs)
          nsubjs.update(subjs)
          
          cur_node = leaf_node
          while cur_node and cur_node.label() != "VP": # traverse tree backwards until containing VP is found
            cur_node = cur_node.parent()
          if cur_node:
            v_vp_map[index] = cur_node
            for subj in subjs:
              nn_vp_map[subj].append(cur_node)

    print "tokens:",  tokens
    print  "="*60
    
    sentence_features = []
    for nn in nsubjs:
      nn_compound = nn_compound_map[nn] if nn in nn_compound_map else tokens[nn]
      amod_jjs = [tokens[jj] for jj in nn_amods[nn]]
      cop_jjs = [tokens[jj] for jj in nn_jj_map[nn]]
      sentence_features.append((nn_compound, amod_jjs, cop_jjs))
      
      print "\tNP={}\n\t\t[JJ]={}".format(nn_compound, (amod_jjs, cop_jjs))
    sentence_info = (tokens, sentence_features)
    results.append(sentence_info)
  reviews_processed.append((review_json, results))
review_file.close()

outfilename = "{}_{}_{:%Y-%m-%d_%H-%M-%S}.pickle".format(sys.argv[0].split('/')[0], filename, datetime.now())
outfilepath = OUTPUT_DIR + "/" + outfilename
with open(outfilepath, 'w+') as outfile:
  pickle.dump(reviews_processed, outfile, -1)

time_elapsed = time.time() - start_time
print "Time elapsed (s): {}".format(time_elapsed)
print "\tApprox {}s per review".format(time_elapsed/len(reviews_processed))
