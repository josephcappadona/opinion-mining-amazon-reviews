# Converts the json review file into LineSentence format, one line = one sentence
import json
import re
import time

review_file = open("../../../../data/reviews_Electronics.json", "r")
output_file = open("./results/reviews_data_word2vec.txt", "w")
pattern = re.compile("[.?!]")
i = 0

def clean(word):
	if word.isalpha():
		return word.lower()	

start = time.time()
for line in review_file:
	review_json = json.loads(line)
	sentences = pattern.split(review_json["reviewText"])	
	for sentence in sentences:
		words = sentence.split()
		for word in words:
			cleaned_word = clean(word)
			if (cleaned_word != None):
				output_file.write(cleaned_word + " ")	
	i += 1
	if (i % 100000 == 0):
		print("Processing " + str(i) + "th review")
end = time.time()
time_taken = end - start
print("Time to process reviews was " + str(time_taken) + " seconds")

review_file.close()
output_file.close()
