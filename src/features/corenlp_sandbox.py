from collections import defaultdict
from pycorenlp import StanfordCoreNLP
import pickle
import time
import sys

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

  # results = []
  # for sentence in parse['sentences']:
  #   sentence_parse = sentence['parse']
  #   print(sentence_parse)
review_file.close()

outfilename = "{}_{}_{:%Y-%m-%d_%H-%M-%S}.pickle".format(sys.argv[0].split('/')[0], filename, datetime.now())
outfilepath = OUTPUT_DIR + "/" + outfilename
with open(outfilepath, 'w+') as outfile:
  pickle.dump(reviews_processed, outfile, -1)

time_elapsed = time.time() - start_time
print "Time elapsed (s): {}".format(time_elapsed)
print "\tApprox {}s per review".format(time_elapsed/len(reviews_processed))
