import nltk
from nltk.parse import corenlp
from utils import is_sentiment_bearing, get_base_lexicons
from collections import defaultdict

LEXICON_FILEPATH = 'lexicon.txt'
CLUSTER_FILEPATH = ''
OUTPUT_DIR = 'output'
MIN_OCCURRENCE_THRESHOLD = 0.05

nltk.download('punkt', quiet=True)

nlp = corenlp.CoreNLPDependencyParser(url='http://localhost:9000')
base_lexicons = get_base_lexicons(LEXICON_FILEPATH)
positive_lexicon, negative_lexicon, neutral_lexicon = base_lexicons

class CorpusInfo(object):

    def __init__(self, reviews):

        self.reviews = reviews
        self.sentences = []

        self.review_id_to_sentence_ids = {}
        self.review_id_to_sentence_dependencies = {}

        self.sentence_id_to_review_id = {}
        self.sentence_id_to_dependencies = {}

    def extract_dependency_information(self):

        for review_id, review in enumerate(self.reviews):
            if (review_id + 1) % (int(len(self.reviews) / 10) + 1) == 0:
                print('Processing review %d of %d' % (review_id + 1, len(self.reviews)))

            review_sentences = nltk.tokenize.sent_tokenize(review)
            review_sentence_ids = []
            review_sentence_dependencies = []
            for sentence in review_sentences:

                self.sentences.append(sentence)

                sentence_id = len(self.sentences) - 1
                self.sentence_id_to_review_id[sentence_id] = review_id
                review_sentence_ids.append(sentence_id)

                print(sentence_id, sentence)
                sentence_dependencies = self.extract_noun_adj_dependencies(sentence)
                review_sentence_dependencies.append(sentence_dependencies)
                self.sentence_id_to_dependencies[sentence_id] = sentence_dependencies
                print('\n')

            self.review_id_to_sentence_ids[review_id] = review_sentence_ids
            self.review_id_to_sentence_dependencies[review_id] = review_sentence_dependencies

    @staticmethod
    def extract_noun_adj_dependencies(sentence):
        
        JJ_to_NN = {}
        NN_to_JJ = {}
        JJ_to_JJs = defaultdict(list)
        NN_to_NNs = defaultdict(list)

        sentence_parse, = nlp.raw_parse(sentence)
        trips = list(sentence_parse.triples()); print(trips)
        for (gov, gov_PoS), dependency, (dep, dep_PoS) in trips:

            if not gov.isalpha() or not dep.isalpha():
                continue

            gov = gov.lower()
            dep = dep.lower()
            gov_PoS = gov_PoS[:2]
            dep_PoS = dep_PoS[:2]
            if dependency == 'nsubj' and dep_PoS == 'NN' and gov_PoS == 'JJ':
                JJ_to_NN[gov] = dep
                NN_to_JJ[dep] = gov
            elif dependency == 'amod' and gov_PoS == 'NN' and dep_PoS == 'JJ':
                JJ_to_NN[dep] = gov
                NN_to_JJ[gov] = dep
            elif dependency == 'conj':
                if gov_PoS == 'JJ' and dep_PoS == 'JJ':
                    JJ_to_JJs[gov].append(dep)
                    JJ_to_JJs[dep].append(gov)
                elif gov_PoS == 'NN' and dep_PoS == 'NN':
                    NN_to_NNs[gov].append(dep)
                    NN_to_NNs[dep].append(gov)

        return JJ_to_NN, NN_to_JJ, JJ_to_JJs, NN_to_NNs


###########
##############
##############

class DoublePropagationInfo(object):

    def __init__(self):
        self.review_id_to_feature_sentiments = defaultdict(lambda : defaultdict(list))
        self.sentence_id_to_feature_sentiments = defaultdict(lambda : defaultdict(list))
        self.feature_sentiments_cumulative = defaultdict(int)
        self.feature_to_pos_sentiment_reviews = defaultdict(list)
        self.feature_to_pos_sentiment_sentences = defaultdict(list)
        self.feature_to_neg_sentiment_reviews = defaultdict(list)
        self.feature_to_neg_sentiment_sentences = defaultdict(list)
        self.opinion_sentiments = {}
        self.opinion_sentiments.update({word:1 for word in positive_lexicon})
        self.opinion_sentiments.update({word:-1 for word in negative_lexicon})
        self.opinion_sentiments.update({word:0 for word in neutral_lexicon})
        self.opinion_to_sentence_ids = defaultdict(set)


def extract_features_and_opinions(reviews):
    corpus_info = CorpusInfo(reviews)
    corpus_info.extract_dependency_information
    corpus_info.aggregate_statistics
    dp_info = DoublePropagationInfo
    i = 0
    while True:
        print('DP Iteration #%d' % i)
        new_features, new_opinions = double_propagation_iterate(dp_info, corpus_info)
        if len(new_opinions) == 0 and len(new_features) == 0:
            break
        features.update(new_features)
        opinions.update(new_opinions)
        i += 1

