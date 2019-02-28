from corpus import CorpusInfo
from double_prop import DoublePropagationInfo

reviews = ['The headphones are great. The headphones are big.', 'The headphones are big and fitting. The headphones and cable are high quality.']
corpus_info = CorpusInfo(reviews)
corpus_info.extract_dependency_information()
dp = DoublePropagationInfo()
print(list(dp.iterate(corpus_info)))
print(list(dp.iterate(corpus_info)))
print(list(dp.iterate(corpus_info)))

