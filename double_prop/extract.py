from corpus import CorpusInfo
from double_prop import DoublePropagationInfo

def extract_features_and_opinions(reviews):

    corpus_info = CorpusInfo(reviews)
    corpus_info.extract_dependency_information()

    dp_info = DoublePropagationInfo()

    i = 0
    while True:
        print('DP Iteration #%d' % i)

        new_features, new_opinions = dp_info.iterate(corpus_info)
        if len(new_opinions) == 0 and len(new_features) == 0:
            break

        i += 1

