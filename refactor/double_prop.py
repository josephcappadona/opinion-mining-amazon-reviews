from utils import get_polarity, normalize, get_base_lexicons
from collections import defaultdict


class DoublePropagationInfo(object):

    def __init__(self, base_lexicon_filepath='lexicon.txt'):

        base_lexicons = positive_lexicon, negative_lexicon, neutral_lexicon = get_base_lexicons(base_lexicon_filepath)

        self.features, self.opinions = set(), set.union(*base_lexicons)

        self.review_id_to_feature_sentiments = defaultdict(lambda : defaultdict(list))
        self.sentence_id_to_feature_sentiments = defaultdict(lambda : defaultdict(list))

        self.feature_sentiments = defaultdict(list)

        self.feature_to_pos_sentiment_reviews = defaultdict(list)
        self.feature_to_pos_sentiment_sentences = defaultdict(list)
        
        self.feature_to_neg_sentiment_reviews = defaultdict(list)
        self.feature_to_neg_sentiment_sentences = defaultdict(list)
        
        self.opinion_sentiments = {}
        self.opinion_sentiments.update({word:1 for word in positive_lexicon})
        self.opinion_sentiments.update({word:-1 for word in negative_lexicon})
        self.opinion_sentiments.update({word:0 for word in neutral_lexicon})
        
        self.opinion_to_sentence_ids = defaultdict(set)

    def iterate(dp_info, corpus_info):

        new_opinions = set()
        new_features = set()

        for review_id in range(len(corpus_info.reviews)):

            sentence_info = zip(corpus_info.review_id_to_sentence_ids[review_id],
                                corpus_info.review_id_to_sentence_dependencies[review_id])
            for sentence_id, (JJ_to_NN, NN_to_JJ, JJ_to_JJs, NN_to_NNs) in sentence_info:

                for JJ, NN in JJ_to_NN.items():
                    if JJ in dp_info.opinions: # if we know this JJ is an opinion word

                        if NN not in dp_info.features:
                            new_features.add(NN) # we have found a new feature word

                        # have we processed JJ in this sentence already?
                        if sentence_id not in dp_info.opinion_to_sentence_ids[JJ]:
                            dp_info.opinion_to_sentence_ids[JJ].add(sentence_id)

                            # NN takes polarity of modifying opinion word
                            opinion_sentiment = dp_info.opinion_sentiments[JJ]
                            dp_info.review_id_to_feature_sentiments[review_id][NN].append(opinion_sentiment)
                            dp_info.sentence_id_to_feature_sentiments[sentence_id][NN].append(opinion_sentiment)

                            # add to NN's cumulative sentiment score
                            dp_info.feature_sentiments[NN].append(opinion_sentiment)
                            if opinion_sentiment > 0:
                                dp_info.feature_to_pos_sentiment_reviews[NN].append(review_id)
                                dp_info.feature_to_pos_sentiment_sentences[NN].append(sentence_id)
                            elif opinion_sentiments[opinion] < 0:
                                dp_info.feature_to_neg_sentiment_reviews[NN].append(review_id)
                                dp_info.feature_to_neg_sentiment_sentences[NN].append(sentence_id)

                            yield ('JJ->NN', JJ, NN, opinion_sentiment, review_id, sentence_id)


                for NN, JJ in NN_to_JJ.items():
                    if NN in dp_info.features:

                        if JJ not in dp_info.opinion_sentiments: # if JJ is a new opinion word
                            print('New opinion: %s' % JJ)
                            new_opinions.add(JJ)
                            dp_info.opinion_to_sentence_ids[JJ].add(sentence_id)

                            if dp_info.review_id_to_feature_sentiments[review_id][NN]: # if NN has sentiment in current review
                                # then JJ takes (cumulative) polarity of NN within this review (Homogenous Rule)
                                cumulative_polarity = sum(dp_info.review_id_to_feature_sentiments[review_id][NN])
                            else: # else NN was discovered in another review
                                # JJ takes cumulative polarity of entire review (Intra-review Rule)
                                cumulative_polarity = sum(sentiment for sentiment_list in dp_info.review_id_to_feature_sentiments[review_id].values() for sentiment in sentiment_list)
                            polarity = normalize(cumulative_polarity)
                            dp_info.opinion_sentiments[JJ] = polarity # TODO: ??or VADER polarity??
                            
                            yield ('NN->JJ', NN, JJ, polarity, review_id, sentence_id)


                for JJ_1, JJs in JJ_to_JJs.items():
                    if JJ_1 in dp_info.opinions:

                        dp_info.opinion_to_sentence_ids[JJ_1].add(sentence_id)

                        for JJ_2 in JJs:

                            dp_info.opinion_to_sentence_ids[JJ_2].add(sentence_id)

                            if JJ_2 not in dp_info.opinions:
                                print('New opinion: %s' % JJ_2)
                                new_opinions.add(JJ_2)
                                dp_info.opinion_sentiments[JJ_2] = dp_info.opinion_sentiments[JJ_1]

                                yield ('JJ->JJ', JJ_1, JJ_2, dp_info.opinion_sentiments[JJ_1], review_id, sentence_id)


                for NN_1, NNs in NN_to_NNs.items():

                    if dp_info.review_id_to_feature_sentiments[review_id][NN_1]: # if NN_1 has sentiment in this review
                        for NN_2 in NNs:

                            if NN_2 not in dp_info.features:
                                print('New feature: %s' % NN_2)
                                new_features.add(NN_2)

                            if not dp_info.review_id_to_feature_sentiments[review_id][NN_2]:
                                # Homogenous Rule
                                NN_1_polarity = normalize(sum(dp_info.review_id_to_feature_sentiments[review_id][NN_1]))
                                dp_info.review_id_to_feature_sentiments[review_id][NN_2].append(NN_1_polarity)
                                dp_info.sentence_id_to_feature_sentiments[sentence_id][NN_2].append(NN_1_polarity)
                                dp_info.feature_sentiments[NN_2].append(NN_1_polarity)

                                if NN_1_polarity > 0:
                                    dp_info.feature_to_pos_sentiment_reviews[NN_2].append(review_id)
                                    dp_info.feature_to_pos_sentiment_sentences[NN_2].append(sentence_id)
                                elif NN_1_polarity < 0:
                                    dp_info.feature_to_neg_sentiment_reviews[NN_2].append(review_id)
                                    dp_info.feature_to_neg_sentiment_sentences[NN_2].append(sentence_id)

                                yield ('NN->NN', NN_1, NN_2, NN_1_polarity, review_id, sentence_id)

        dp_info.features.update(new_features)
        dp_info.opinions.update(new_opinions)

