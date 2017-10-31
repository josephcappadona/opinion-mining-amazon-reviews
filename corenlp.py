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
from helper import traverse

# parse args
if len(sys.argv) < 3:
  raise ValueError

MAX_ = 500  # set to number of reviews you want to process (for short tests)
filepath = sys.argv[1]  # path to review data
filename = filepath.split('/')[-1]
OUTPUT_DIR = sys.argv[2]  # path to output directory

from stanford_corenlp_pywrapper import CoreNLP
# for CoreNLP wrapper API, see https://github.com/brendano/stanford_corenlp_pywrapper
proc = CoreNLP("parse", corenlp_jars=["/mnt/castor/seas_home/j/jcapp/Documents/SeniorDesign/CoreNLP/stanford-corenlp-full-2017-06-09/*"])

review_file = open(filepath, 'r')
reviews_processed = []
start_time = time.time()
for review in review_file:
  if len(reviews_processed) >= MAX_:
    break
  review_json = json.loads(review)
  parse = proc.parse_doc(review_json['reviewText'])
  
  print "\n\n{} {}\n------------------".format(review_json['ReviewerID'], review_json['asin'])

  results = []
  for sentence in parse['sentences']:
    tree = ParentedTree.fromstring(sentence['parse'])
    tv = traverse(tree)
    tokens = sentence['tokens']
    
    # glossary of dependencies: http://universaldependencies.org/en/dep/index.html
    # also, for better intuition, play around with http://nlp.stanford.edu:8080/corenlp/process
    #    try sentences like "the sound quality is very poor and is not worth the price"
    nn_amods = defaultdict(list) # maps NN index to list of its children with amod dependency
    nn_np_map = defaultdict(list) # maps NN index to list of NP trees containing it
    nn_jj_map = defaultdict(list) # maps NN index to list of NP trees containing it
    nn_vp_map = defaultdict(list) # maps NN index to VP trees modifying it
    nsubjs = set() # set of tokens (indexes) receiving nsubj dependency
    jj_nsubj = {} # maps JJ index to corresponding nsubj index
    v_nsubj = {} # maps V index to corresponding nsubj index
    v_vp_map = {} # maps V index to tree of VP containing it
    jj_adjp_map = {} # maps JJ index to tree of ADJP containing it
    jj_vp_map = {} # maps JJ index to tree of VP containing it
    
    for index,pos_tag in enumerate(sentence['pos']):
      try:
        leaf_node = next(tv)
      except StopIteration:
        break
      cur_node = leaf_node
      if pos_tag[:2] == "NN":
        for dep,i,j in sentence['deps_cc']:
          if i == index and dep == "amod":
            nn_amods[i].append(j)
            nsubjs.add(index)
        while cur_node:
          if cur_node.label() == "NP":
            nn_np_map[index].append(cur_node)
          cur_node = cur_node.parent()
        
      elif pos_tag[:2] == "JJ":
        for dep,i,j in sentence['deps_cc']:
          if i == index and dep == "nsubj":
            jj_nsubj[index] = j
            nsubjs.add(j)
            nn_jj_map[j].append(index)
            while cur_node and cur_node.label() != "ADJP": #traverse tree backwards until containing ADJP is found
              cur_node = cur_node.parent()
            adjp_node = cur_node
            if adjp_node:
              jj_adjp_map[i] = adjp_node
            while cur_node and cur_node.label() != "VP": # traverse tree backwards until containing ADJP is found
              cur_node = cur_node.parent()
            vp_node = cur_node
            if adjp_node and vp_node:
              jj_vp_map[i] = cur_node


      
      elif pos_tag[:1] == "V":
        for dep,i,j in sentence['deps_cc']:
          if i == index and dep == "nsubj":
            v_nsubj[index] = j
            nsubjs.add(j)
            
            cur_node = leaf_node
            while cur_node and cur_node.label() != "VP": # traverse tree backwards until containing VP is found
              cur_node = cur_node.parent()
            if cur_node:
              v_vp_map[index] = cur_node
              nn_vp_map[j].append(cur_node)

    print tokens
    print  "======"
    sentence_features = {}
    for nn in nsubjs:
      nn_ = defaultdict(list)
      
      nps = [np_tree.leaves() for np_tree in nn_np_map[nn]]
      nn_['np'] = nps
      m = "\tNN: {}".format(tokens[nn], nps)
      if nps:
        m += " ({})".format([' '.join(np) for np in nps])
      print m

      for amod in nn_amods[nn]:
        print "\t\tJJ: {}".format(tokens[amod])
        nn_['jj'].append((tokens[amod], ))

      for jj in nn_jj_map[nn]:
        m = "\t\tJJ: {}".format(tokens[jj])
        p = None
        if jj in jj_vp_map:
          vp = jj_vp_map[jj]
          p = vp
        elif jj in jj_adjp_map:
          adjp = jj_adjp_map[jj]
          if adjp != tokens[jj]:
            p = adjp
          m += " ({})".format(p.leaves())
        nn_['jj'].append((tokens[jj],p.leaves() if p else None))
        print m 
      for vp_tree in nn_vp_map[nn]:
        vp = vp_tree.leaves()
        print "\t\tVP: {}".format(vp)
        nn_['vp'].append(vp)
      print ""
      sentence_features[tuple(tokens[nn])] = nn_
    results.append((tokens, sentence_features))
  reviews_processed.append(results)
review_file.close()

outfilename = "{}_{}_{}.pickle".format(sys.argv[0].split('/')[0], filename, int(time.time()))
outfilepath = OUTPUT_DIR + "/" + outfilename
with open(outfilepath, 'w+') as outfile:
  for review_processed in reviews_processed:
    outfile.write(pickle.dumps(review_processed) + '\n')

time_elapsed = time.time() - start_time
print "Time elapsed (s): {}".format(time_elapsed)
print "\tApprox {}s per review".format(time_elapsed/len(reviews_processed))

