import mysql.connector
import sys
import nltk
import pickle
from pprint import pprint
from nltk.parse.corenlp import CoreNLPDependencyParser
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

if len(sys.argv) < 2:
    print("Usage: python3 double-prop.py review_asin")
    exit()
    
# Constants
PRODUCT_ASIN = sys.argv[1]
LEXICON_FILEPATH = "./lexicon.txt"
CLASS_PICKLE = "./clustering/results/clean-classes.pkl"
MIN_THRESHOLD = 0.05

# Start the CoreNLP server with:
# java -mx4g -cp "./CoreNLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
#     (on my Mac, java8 bin located at /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java)
nlp = CoreNLPDependencyParser(url="http://localhost:9000")

# Open connection to db
config = {
    "user": "root",
    "password": "root",
    "host": "127.0.0.1",
    "database": "senior_design"
}
connection = mysql.connector.connect(**config)
cursor = connection.cursor(buffered=True)

# Get reviews and lexicons and clusters
def get_all_reviews(asin):
    query = "SELECT review_text FROM review WHERE asin = '{}'".format(asin)
    cursor.execute(query)
    reviews = []
    for (review_text) in cursor:
        reviews.append(review_text[0])
    print("# reviews: {}".format(len(reviews)))
    return reviews

def parse_lexicons(filepath):
    with open(filepath, "r") as f:
        positive_lexicon = {x for x in f.readline().split()}
        f.readline()
        negative_lexicon = {x for x in f.readline().split()}
        f.readline()
        neutral_lexicon = {x for x in f.readline().split()}
        return positive_lexicon, negative_lexicon, neutral_lexicon

def get_sorted_classes(features_count, MIN_NUM_REVIEWS):
    frequent_features = [(f, cnt) for f, cnt in features_count.items() if cnt >= MIN_NUM_REVIEWS]
    features_by_class = dict()
    not_found = set()

    # features_by_class is a dict from class number -> [feature list, total count]
    for feature, cnt in frequent_features:
        if feature not in feature_to_class:
            not_found.add(feature)
            continue
        class_num = feature_to_class[feature]
        if class_num not in features_by_class:
            features_by_class[class_num] = [[], 0]
        features_by_class[class_num][0].append(feature)
        features_by_class[class_num][1] += cnt

    sorted_classes = sorted(features_by_class.values(), key=lambda x: x[1], reverse=True)
    print("Not found in any cluster: " + str(not_found))
    return sorted_classes

def is_sentiment_bearing(adj):
    if adj in neutral_lexicon:
        return False
    for ss in wn.synsets(adj):
        if ss.pos() == "a" or ss.pos() == "s":
            return True
    return False

def filter_opinions(opinions, opinion_sentiments):
    is_sentiment_bearing_dict = {opinion: is_sentiment_bearing(opinion) for opinion in opinions}
    for opinion, result in is_sentiment_bearing_dict.items():
        if not result:
            opinions.remove(opinion)
            del opinion_sentiments[opinion]
    
reviews = get_all_reviews(PRODUCT_ASIN)
positive_lexicon, negative_lexicon, neutral_lexicon = parse_lexicons(LEXICON_FILEPATH)
feature_to_class = pickle.load(open(CLASS_PICKLE, "rb"))

# DOUBLE-PROPAGATION
# input: parsed_sentence, cumulative information dictionaries (FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count)
# output: extracted dependency features
def extract_relevant_dependencies(parsed_sentence, FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count):
    extracted_sentence = []
    for (gov, gov_pos), dependency, (dep, dep_pos) in parsed_sentence.triples():
        if not gov.isalpha() or not dep.isalpha():
            continue
        gov = gov.lower()
        dep = dep.lower()
        if dependency == "nsubj" and dep_pos == "NN":
            OF_dict[gov] = dep
            FO_dict[dep] = gov
            features_count[dep] += 1
            opinions_count[gov] += 1
        elif dependency == "amod" and gov_pos == "NN":
            OF_dict[dep] = gov
            FO_dict[gov] = dep
            opinions_count[dep] += 1
            features_count[gov] += 1
        elif dependency == "conj":
            if gov_pos == "JJ" and dep_pos == "JJ":
                OO_dict[gov].append(dep)
                OO_dict[dep].append(gov)
                opinions_count[gov] += 1
                opinions_count[dep] += 1
            elif gov_pos == "NN" and dep_pos == "NN":
                FF_dict[gov].append(dep)
                FF_dict[dep].append(gov)
                features_count[gov] += 1
                features_count[dep] += 1
        extracted_sentence.append(((gov, gov_pos), dependency, (dep, dep_pos)))
    #parsed_sentences.append(extracted_sentence)
    return extracted_sentence


# input: all_review_info, cumulative information dictionaries
# output: new_features, new_opinions
def double_propagation_iterate(all_review_info,
                               features,
                               feature_words_by_review,
                               feature_sentiments_by_review,
                               feature_sentiments_cumulative,
                               feature_sentiments_pos,
                               feature_sentiments_neg,
                               opinions,
                               opinion_words_by_review,
                               opinion_sentiments):
    new_opinions = set()
    new_features = set()

    for index, info in all_review_info.items():
        feature_sentiments_by_review[index] = defaultdict(int)

        for opinion, feature in info['OF_dict'].items():
            if opinion in opinions:
                if feature not in features:
                    new_features.add(feature)

                if feature not in feature_words_by_review[index]:
                    feature_words_by_review[index].add(feature)

                    # target takes polarity of modifying opinion word
                    feature_sentiments_by_review[index][feature] = opinion_sentiments[opinion]
                    # add to target's cumulative sentiment score
                    feature_sentiments_cumulative[feature] += opinion_sentiments[opinion]
                    if opinion_sentiments[opinion] > 0:
                        feature_sentiments_pos[feature].append(info['index'])
                    elif opinion_sentiments[opinion] < 0:
                        feature_sentiments_neg[feature].append(info['index'])

                # have we seen this opinion word in this review?
                if opinion not in opinion_words_by_review[index]:
                    opinion_words_by_review[index].add(opinion)
                    info['cumulative_polarity'] += opinion_sentiments[opinion]

        for opinion1, related in info['OO_dict'].items():
            if opinion1 in opinions:
                for opinion in related:
                    if opinion not in opinions:
                        new_opinions.add(opinion)
                        opinion_sentiments[opinion] = opinion_sentiments[opinion1]

                    # have we seen this opinion word in this review?
                    if opinion not in opinion_words_by_review[index]:
                        opinion_words_by_review[index].add(opinion)
                        info['cumulative_polarity'] += opinion_sentiments[opinion]

                # have we seen this opinion word in this review?
                if opinion1 not in opinion_words_by_review[index]:
                    opinion_words_by_review[index].add(opinion1)
                    info['cumulative_polarity'] += opinion_sentiments[opinion1]

        for feature, opinion in info['FO_dict'].items():
            if feature in features:
                if opinion not in opinions:
                    new_opinions.add(opinion)

                    # if target has sentiment in current review
                    if feature in feature_words_by_review[index]:
                        # then opinion takes polarity of target (Homogenous Rule)
                        opinion_sentiments[opinion] = feature_sentiments_by_review[index][feature]
                    else:
                        # else target is from another review
                        # opinion takes cumulative sentiment of entire review (Intra-review Rule)
                        try:
                            cumulative_polarity = int(info['cumulative_polarity'] / abs(info['cumulative_polarity']))
                        except ZeroDivisionError:
                            cumulative_polarity = 0
                        opinion_sentiments[opinion] = cumulative_polarity

                        # also apply that polarity to the feature (should we do this?)
                        feature_words_by_review[index].add(feature)
                        feature_sentiments_by_review[index][feature] = opinion_sentiments[opinion]
                        # add to target's cumulative sentiment
                        feature_sentiments_cumulative[feature] += opinion_sentiments[opinion]
                        if opinion_sentiments[opinion] > 0:
                            feature_sentiments_pos[feature].append(info['index'])
                        elif opinion_sentiments[opinion] < 0:
                            feature_sentiments_neg[feature].append(info['index'])

                if opinion not in opinion_words_by_review[index]:
                    opinion_words_by_review[index].add(opinion)
                    info['cumulative_polarity'] += opinion_sentiments[opinion]

                if feature not in feature_sentiments_by_review[index]:
                    feature_words_by_review[index].add(feature)
                    feature_sentiments_by_review[index][feature] = opinion_sentiments[opinion]
                    # add to target's cumulative sentiment
                    feature_sentiments_cumulative[feature] += opinion_sentiments[opinion]
                    if opinion_sentiments[opinion] > 0:
                        feature_sentiments_pos[feature].append(info['index'])
                    elif opinion_sentiments[opinion] < 0:
                        feature_sentiments_neg[feature].append(info['index'])

        for feature1, related in info['FF_dict'].items():
            if feature1 in features and feature1 in feature_sentiments_by_review[index]:
                for feature in related:
                    if feature not in features:
                        new_features.add(feature)

                    # have we seen this target word in this review?
                    if feature not in feature_words_by_review[index]:
                        feature_words_by_review[index].add(feature)

                        # Homogenous Rule
                        feature_sentiments_by_review[index][feature] = feature_sentiments_by_review[index][feature1]
                        feature_sentiments_cumulative[feature] += feature_sentiments_by_review[index][feature]
                        if feature_sentiments_by_review[index][feature] > 0:
                            feature_sentiments_pos[feature].append(info['index'])
                        elif feature_sentiments_by_review[index][feature] < 0:
                            feature_sentiments_neg[feature].append(info['index'])
    return new_features, new_opinions


# input: list of review texts
# output: all features, expanded opinion lexicon
def extract_features_opinions(reviews):
    features = set()
    features_count = defaultdict(int)
    opinions = positive_lexicon.union(negative_lexicon)
    opinions_count = defaultdict(int)
    
    raw_sentences = []
    parsed_sentences = []
    parses = []
    review_indices = []
    review_info = {} # store info about deps on per review basis
    for i, review in enumerate(reviews):
        if i % 500 == 0:
            print("Processing review: " + str(i))
        OF_dict = {}
        FO_dict = {}
        OO_dict = defaultdict(list)
        FF_dict = defaultdict(list)
        
        raw_sentences.extend(sent_tokenize(review))
        parse = nlp.parse_text(review)
        parses.append(parse)
        for sentence in parse:
            # extract relevant dependency information
            extracted_sentence = extract_relevant_dependencies(sentence, FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count)
            
            review_indices.append(i)
            parsed_sentences.append(extracted_sentence)

        review_info[i] = { 'index' : i,
                           'OF_dict' : OF_dict,
                           'FO_dict' : FO_dict,
                           'OO_dict' : OO_dict,
                           'FF_dict' : FF_dict,
                           'cumulative_polarity' : 0 }

    # instantiate cumulative data structures
    i = 0
    feature_sentiments_by_review = defaultdict(dict) # same sentiment for target words within review (this is an assumption [Observation 1])
    feature_sentiments_cumulative = defaultdict(int)
    feature_sentiments_pos = defaultdict(list) # keep track of the review indices that contributed negative sentiments toward each feature
    feature_sentiments_neg = defaultdict(list) # keep track of the review indices that contributed negative sentiments toward each feature
    feature_words_by_review = defaultdict(set) # keep track of the feature words in each review
    opinion_words_by_review = defaultdict(set) # keep track of the opinion words in each review
    opinion_sentiments = {} # same sentiment for opinion words throughout the corpus (this is an assumption [Observation 2])
    opinion_sentiments.update({op:(1 if op in positive_lexicon else -1) for op in opinions})

    while (True):
        print("DP Iteration: {}".format(i))
        i += 1

        # double propagation step
        new_features, \
        new_opinions = double_propagation_iterate(review_info,
                                                  features,
                                                  feature_words_by_review,
                                                  feature_sentiments_by_review,
                                                  feature_sentiments_cumulative,
                                                  feature_sentiments_pos,
                                                  feature_sentiments_neg,
                                                  opinions,
                                                  opinion_words_by_review,
                                                  opinion_sentiments)
        
        features = features.union(new_features)
        opinions = opinions.union(new_opinions)
        if len(new_opinions) == 0 and len(new_features) == 0:
            break

    res = (features,
           features_count,
           opinions,
           opinions_count,
           raw_sentences,
           parsed_sentences,
           review_indices,
           feature_sentiments_by_review,
           feature_words_by_review,
           feature_sentiments_cumulative,
           feature_sentiments_pos,
           feature_sentiments_neg,
           opinion_words_by_review,
           opinion_sentiments)
    return res

# DOUBLE-PROP OUTPUTS
features, \
features_count, \
opinions, \
opinions_count, \
raw_sentences, \
parsed_sentences, \
review_indices, \
feature_sentiments_by_review, \
feature_words_by_review, \
feature_sentiments_cumulative, \
feature_sentiments_pos, \
feature_sentiments_neg, \
opinion_words_by_review, \
opinion_sentiments = extract_features_opinions(reviews)

# PRINTS
print("Feature clusters:")
sorted_classes = get_sorted_classes(features_count, MIN_THRESHOLD * len(reviews))
pprint(sorted_classes)

filter_opinions(opinions, opinion_sentiments)
lexicon = positive_lexicon.union(negative_lexicon)
print("Opinion word sentiments (newly discovered):")
pprint(sorted([(opinion, sentiment) for opinion, sentiment in opinion_sentiments.items() if opinion not in lexicon], key=lambda x:x[1], reverse=False))