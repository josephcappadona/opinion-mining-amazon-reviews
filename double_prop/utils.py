import nltk
from nltk.sentiment import vader

# NLTK VADER sentiment analysis reference: http://www.nltk.org/howto/sentiment.html
nltk.download('vader_lexicon', quiet=True)
sentiment_analyzer = vader.SentimentIntensityAnalyzer()
SENTIMENT_THRESHOLD = 0.1

def is_sentiment_bearing(adj, sentiment_threshold=SENTIMENT_THRESHOLD):
    polarity_scores = sentiment_analyzer.polarity_scores(adj)
    polarity = polarity_scores['compound']
    return abs(polarity) > sentiment_threshold

def get_polarity(adj, sentiment_threshold=SENTIMENT_THRESHOLD):

    vader_polarity = sentiment_analyzer.polarity_scores(adj)['compound']
    if vader_polarity > sentiment_threshold:
        return 1
    elif vader_polarity < -sentiment_threshold:
        return -1
    else:
        return 0

def normalize(integer):
    try:
        return int(integer / abs(integer))
    except ZeroDivisionError:
        return 0

def get_base_lexicons(filepath):
    with open(filepath, 'r') as f:
        positive_lexicon = {x for x in f.readline().split()}
        f.readline()
        negative_lexicon = {x for x in f.readline().split()}
        f.readline() 
        neutral_lexicon = {x for x in f.readline().split()}
        return positive_lexicon, negative_lexicon, neutral_lexicon
        
