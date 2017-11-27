"""Detect sentiment for adjectives.

1st approach: CoreNLP doesn't seem to provide sentiment polarity.

2nd approach: VADER

"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def get_score(adjective):
    """Returns a compound score [-1, 1] representing how negative/positive the
    adjective is.

    """
    return analyzer.polarity_scores(adjective)['compound']


adjectives = [
    'fantastic',
    'okay',
    'good',
    'fine',
    'awesome',
    'superb',
    'perfect',
    'horrible',
    'terrible',
    'disgusting',
    'flimsy',
]

for adjective in adjectives:
    print(
        'Adjective: ',
        adjective,
        'Sentiment:',
        get_sentiment_score(adjective)
    )

"""
Output:
('Adjective: ', 'fantastic', 'Sentiment:', 0.5574)
('Adjective: ', 'okay', 'Sentiment:', 0.2263)
('Adjective: ', 'good', 'Sentiment:', 0.4404)
('Adjective: ', 'fine', 'Sentiment:', 0.2023)
('Adjective: ', 'awesome', 'Sentiment:', 0.6249)
('Adjective: ', 'superb', 'Sentiment:', 0.6249)
('Adjective: ', 'perfect', 'Sentiment:', 0.5719)
('Adjective: ', 'horrible', 'Sentiment:', -0.5423)
('Adjective: ', 'terrible', 'Sentiment:', -0.4767)
('Adjective: ', 'disgusting', 'Sentiment:', -0.5267)
('Adjective: ', 'flimsy', 'Sentiment:', 0.0)
"""
