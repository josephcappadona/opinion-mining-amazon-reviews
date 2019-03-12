from sys import argv as args
from os import makedirs
import json
from nltk.tokenize import sent_tokenize, word_tokenize

def get_reviews(reviews_filepath):
    with open(reviews_filepath, 'rt') as reviews_file:
        for line in reviews_file:
            if line:
                review_json = json.loads(line)
                yield review_json['reviewText']

def clean_sentence(sentence):
    cleaned_words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
    return ' '.join(cleaned_words)

def clean_corpus(reviews):
    for review in reviews:
        for sentence in sent_tokenize(review):
            cleaned_sentence = clean_sentence(sentence)
            yield cleaned_sentence

def get_directory(filepath):
    return '/'.join(filepath.split('/')[:-1])

if __name__ == '__main__':
    
    if len(args) != 3:
        print('USAGE:  python preprocess_corpus.py REVIEWS_FILEPATH.json OUTPUT_FILEPATH.txt')
        exit()
    reviews_filepath = args[1]
    output_filepath = args[2]

    output_directory = get_directory(output_filepath)
    if output_directory: makedirs(output_directory, exist_ok=True)

    reviews = get_reviews(reviews_filepath)
    num_reviews = 0
    num_sentences = 0
    with open(output_filepath, 'wt+') as output_file:
        for review in reviews:
            num_reviews += 1
            if (num_reviews-1) % 1000 == 0: print('Processing review #%d' % (num_reviews))
            for sentence in sent_tokenize(review):
                num_sentences += 1
                cleaned_sentence = clean_sentence(sentence)
                output_file.write(cleaned_sentence + '\n')
print('Output %d sentences for %d reviews to \'%s\'' % (num_sentences, num_reviews, output_filepath))
