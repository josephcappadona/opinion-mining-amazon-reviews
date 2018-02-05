import math
import statistics

# from . import liwc
from . import adjective


def weight_score(score, num_helpful, num_unhelpful):
    """
    Log weighting idea from reddit ranking algorithm:
    https://medium.com/hacking-and-gonzo/how-reddit-ranking-algorithms-work-ef111e33d0d9

    TODO(ryin): try better heuristics
    - consider using threshold

    """

    net = num_helpful - num_unhelpful
    order = math.log(max(net, 2), 2)
    return order


def get_weighted_sentiment(product_feature_adjs):
    """
    Returns weighted sentiment scores for each product feature of the product.
    product_feature_adjs: list of (feature, [([adjectives...], [# helpful, # unhelpful], review score)])

    output: [(feature, score in [-1, 1])] sorted in descending score


    ryin: 1st pass algorithm (11/27)
        for each product quality and adj list:
        for each (adj, helpful score, review score):
            1. find sentiment valence [-1, 1] for each adjective.
                - if sentiment valence differs significantly from review score, print out
            2. weight by helpful score
                * Initial pass (11/27): if helpful ratio > 0.5, add (# helpful) - 0.5 (# unhelpful)
                    TODO(ryin): improve this.

    """
    wc = Counter()
    total_num = total_denom = 0
    feature_scores = []
    for product_quality, adj_data in feat_adjs:
        for adjectives, (num_helpful, num_total), review_score in adj_data:
            scores = [adjective.get_score(
                adjective) for adjective in adjectives]
            score = statistics.mean(scores)
            # TODO: log weird ones that differ from review score, or have
            # weird varying scores, etc
            weight = weight_score(score, num_helpful, num_total - num_helpful)
            wc[weight] += 1
            total_num += score * weight
            total_denom += weight
        final_score = len(adj_data) * float(total_num) / total_denom
        feature_scores.append((product_quality, final_score))

    print(wc)  # Distribution of weights

    return sorted(feature_scores, key=lambda item: item[1], reverse=True)
