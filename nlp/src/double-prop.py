import mysql.connector
import sys
import nltk
import pickle
import json
import pathlib2 as pathlib
from pprint import pprint
from nltk.parse.corenlp import CoreNLPDependencyParser
from collections import defaultdict
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn

if len(sys.argv) < 2:
    print("Usage: python3 double-prop.py review_asin")
    exit()

# Constants
PRODUCT_ASIN = sys.argv[1]
LEXICON_FILEPATH = "./lexicon.txt"
CLASS_PICKLE = "./clustering/results/clean-classes.pkl"
OUTPUT_DIR = "../output"
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

nltk.download('wordnet')

pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

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


# DOUBLE-PROPAGATION
# input: parsed_sentence, cumulative information dictionaries (FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count)
# output: extracted dependency features
def extract_relevant_dependencies(parsed_sentence, FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count, feature_opinions):
    extracted_sentence = []
    for (gov, gov_pos), dependency, (dep, dep_pos) in parsed_sentence.triples():
        if not gov.isalpha() or not dep.isalpha():
            continue
        gov = gov.lower()
        dep = dep.lower()
        if dependency == "nsubj" and dep_pos == "NN" and gov_pos == "JJ" and is_sentiment_bearing(gov):
            OF_dict[gov] = dep
            FO_dict[dep] = gov
            features_count[dep] += 1
            opinions_count[gov] += 1
            feature_opinions[dep].append(gov)
        elif dependency == "amod" and gov_pos == "NN" and dep_pos == "JJ" and is_sentiment_bearing(dep):
            OF_dict[dep] = gov
            FO_dict[gov] = dep
            opinions_count[dep] += 1
            features_count[gov] += 1
            feature_opinions[gov].append(dep)
        elif dependency == "conj":
            if gov_pos == "JJ" and dep_pos == "JJ" and is_sentiment_bearing(gov) and is_sentiment_bearing(dep):
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
    feature_opinions = defaultdict(list)

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
            extracted_sentence = extract_relevant_dependencies(sentence, FO_dict, OF_dict, FF_dict, OO_dict, features_count, opinions_count, feature_opinions)

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
           opinion_sentiments,
           feature_opinions)
    return res


def process_asin(asin):
    print('Processing {}'.format(asin))
    product_reviews = get_all_reviews(asin)

    product_info = {'asin':asin}
    product_info['features'], \
    product_info['features_count'], \
    product_info['opinions'], \
    product_info['opinions_count'], \
    product_info['raw_sentences'], \
    product_info['parsed_sentences'], \
    product_info['review_indices'], \
    product_info['feature_sentiments_by_review'], \
    product_info['feature_words_by_review'], \
    product_info['feature_sentiments_cumulative'], \
    product_info['feature_sentiments_pos'], \
    product_info['feature_sentiments_neg'], \
    product_info['opinion_words_by_review'], \
    product_info['opinion_sentiments'], \
    product_info['feature_opinions'] = extract_features_opinions(product_reviews)

    product_info['features_by_count'] = sorted(product_info['features_count'].items(), key=lambda x: x[1], reverse=True)
    product_info['sorted_classes'] = get_sorted_classes(product_info['features_count'], MIN_THRESHOLD * len(product_reviews))

    return product_info



feature_to_class = pickle.load(open(CLASS_PICKLE, "rb"))
positive_lexicon, negative_lexicon, neutral_lexicon = parse_lexicons(LEXICON_FILEPATH)

###########################
### DOUBLE-PROP OUTPUTS ###
###########################
product_info = process_asin(PRODUCT_ASIN)

features = product_info['features']
features_count = product_info['features_count']
opinions = product_info['opinions']
opinions_count = product_info['opinions_count']
raw_sentences = product_info['raw_sentences']
parsed_sentences = product_info['parsed_sentences']
review_indices = product_info['review_indices']
feature_sentiments_by_review = product_info['feature_sentiments_by_review']
feature_words_by_review = product_info['feature_words_by_review']
feature_sentiments_cumulative = product_info['feature_sentiments_cumulative']
feature_sentiments_pos = product_info['feature_sentiments_pos']
feature_sentiments_neg = product_info['feature_sentiments_neg']
opinion_words_by_review = product_info['opinion_words_by_review']
opinion_sentiments = product_info['opinion_sentiments']
feature_opinions = product_info['feature_opinions']
features_by_count = product_info['features_by_count']
sorted_classes = product_info['sorted_classes']

#############
### PRINTS ##
#############
print("Feature clusters:")
pprint(sorted_classes)

# Set of features that made it into a cluster
final_features = set()
for cluster, count in sorted_classes:
    for feature in cluster:
        final_features.add(feature)
for feature in list(feature_opinions.keys()):
    if feature not in final_features:
        del feature_opinions[feature]
# Set of opinions related to features in a cluster
final_opinions = set()
for opinions in feature_opinions.values():
    for opinion in opinions:
        final_opinions.add(opinion)

#filter_opinions(opinions, opinion_sentiments)
lexicon = positive_lexicon.union(negative_lexicon)
print("Opinion word sentiments (newly discovered):")
pprint(sorted([(opinion, sentiment) for opinion, sentiment in opinion_sentiments.items()
               if opinion not in lexicon and opinion in final_opinions], key=lambda x:x[1], reverse=False))

for feature, opinions in feature_opinions.items():
    for i, opinion in enumerate(opinions):
        if opinion in opinion_sentiments:
            opinions[i] = (opinion, opinion_sentiments[opinion])
        else:
            print("Error, " + opinion + " missing from sentiment list")
pprint(feature_opinions)




#################################
### BUILD TABLES FOR DATABASE ###
#################################

# word2vec class table
def get_class_table(feature_to_class):
    classes = defaultdict(list)
    for feature, class_ in feature_to_class.items():
        classes[class_].append(feature)
    classes = sorted(classes.items(), key=lambda x: x[0])

    return classes


# product quality cluster table
def get_quality_clusters_table(asin, product_info):
    quality_clusters = []

    clusters_dict = defaultdict(list)
    feature_to_class = pickle.load(open("./clustering/results/classes.pkl", "rb"))
    features_by_count = sorted(product_info['features_count'].items(), key=lambda x:x[1], reverse=True)
    for feature, _ in features_by_count:
        try:
            class_of_feature = feature_to_class[feature]
            clusters_dict[class_of_feature].append(feature)
        except KeyError:
            pass
    clusters = list(clusters_dict.values())

    class_of_cluster = {}
    clusters_inverse = {}
    cluster_sentiments = {}
    for id_, cluster_features in enumerate(clusters):
        cluster_sentiment = [0, 0] # [pos, neg]
        for feature in cluster_features:
            clusters_inverse[feature] = id_
            class_of_cluster[id_] = feature_to_class[feature]
            cluster_sentiment[0] += len(product_info['feature_sentiments_pos'][feature])
            cluster_sentiment[1] += len(product_info['feature_sentiments_neg'][feature])
        cluster_sentiments[id_] = cluster_sentiment
    for cluster_id, sentiments in cluster_sentiments.items():
        class_id = class_of_cluster[cluster_id]
        cluster_features = clusters_dict[class_id]
        num_positive = cluster_sentiments[cluster_id][0]
        num_negative = cluster_sentiments[cluster_id][1]
        quality_clusters.append((asin, class_id, cluster_id, cluster_features, num_positive, num_negative))
    product_info['cluster_sentiments'] = cluster_sentiments
    product_info['class_of_cluster'] = class_of_cluster
    product_info['clusters'] = clusters
    return quality_clusters


# product-quality relationship table
def get_product_quality_table(asin, product_info):
    product_quality_relationships = []
    clusters = product_info['clusters']
    cluster_sentiments = product_info['cluster_sentiments']
    class_of_cluster = product_info['class_of_cluster']
    for id_, cluster in enumerate(clusters):
        quality_cluster_id = id_
        quality_list = clusters[id_]
        num_positive = cluster_sentiments[id_][0]
        num_negative = cluster_sentiments[id_][1]

        for feature in cluster:
            quality = feature
            quality_class_id = class_of_cluster[id_]
            num_positive = len(product_info['feature_sentiments_pos'][feature])
            num_negative = len(product_info['feature_sentiments_neg'][feature])
            product_quality_relationships.append((asin, quality, quality_cluster_id, quality_class_id, num_positive, num_negative))
    return product_quality_relationships



# CLASS TABLE
# build table
class_table_columns = ['id', 'quality_list']
class_table = get_class_table(feature_to_class)

# write to file
with open('{}/class_table.json'.format(OUTPUT_DIR), 'w') as class_table_file:
    json.dump(dict(zip(class_table_columns, class_table)), class_table_file)


# QUALITY CLUSTER TABLE
# build table
quality_clusters_table_columns = ['asin', 'class_id', 'quality_cluster_id', 'quality_list', 'num_positive', 'num_negative']
quality_clusters_table = get_quality_clusters_table(PRODUCT_ASIN, product_info)

# write to file
quality_clusters_table_directory = '{}/quality_clusters'.format(OUTPUT_DIR)
pathlib.Path(quality_clusters_table_directory).mkdir(parents=True, exist_ok=True)
with open('{}/{}.json'.format(quality_clusters_table_directory, PRODUCT_ASIN), 'w') as quality_clusters_table_file:
    json.dump(dict(zip(quality_clusters_table_columns, quality_clusters_table)), quality_clusters_table_file)


# PRODUCT QUALITY TABLE
# build table
product_quality_relationship_table_columns = ['asin', 'quality', 'quality_cluster_id', 'class_id', 'num_positive', 'num_negative']
product_quality_table = get_product_quality_table(PRODUCT_ASIN, product_info)

# write to file
product_quality_table_directory = '{}/product_qualities'.format(OUTPUT_DIR)
pathlib.Path(product_quality_table_directory).mkdir(parents=True, exist_ok=True)
with open('{}/{}.json'.format(product_quality_table_directory, PRODUCT_ASIN), 'w') as product_quality_table_file:
    json.dump(dict(zip(product_quality_relationship_table_columns, product_quality_table)), product_quality_table_file)



################################
### GET REVIEW TEXT SNIPPETS ###
################################

# If k is defined, the method will return snippets for the top k most common features
# If l is defined, it will return snippets containing words in l
# Outputs a list of tuples of the form:
#    (asin, feature, review_id, sentence_id, sentence, polarity)
def get_snippet_table(asin, product_info, k=15, l=[]):
    snippets = []

    raw_sentences = product_info['raw_sentences']
    review_indices = product_info['review_indices']
    top_features_by_count = [feature for feature,cnt in sorted(product_info['features_count'].items(), key=lambda x:x[1], reverse=True)]

    feature_set = set()
    feature_set.union(top_features_by_count[:k])
    feature_set.union(l)

    for sentence_id, (sentence,review_id) in enumerate(zip(raw_sentences,review_indices)):
        for word in word_tokenize(sentence):
            word = word.lower()
            if word in feature_set and word in product_info['features']:
                polarity = product_info['feature_sentiments_by_review'][review_id][word]
                snippets.append((asin, word, review_id, sentence_id, sentence, polarity))

    return snippets


# build snippet table
snippet_table_columns = ['asin', 'quality', 'review_id', 'sentence_id', 'sentence', 'polarity']
snippet_table = get_snippet_table(PRODUCT_ASIN, product_info)

# write to file
snippet_table_directory = '{}/snippets'.format(OUTPUT_DIR)
pathlib.Path(snippet_table_directory).mkdir(parents=True, exist_ok=True)
with open('{}/{}.json'.format(snippet_table_directory, PRODUCT_ASIN), 'w') as snippet_table_file:
    json.dump(dict(zip(snippet_table_columns, snippet_table)), snippet_table_file)



