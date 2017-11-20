import spacy
import csv
import pickle

nlp = spacy.load('en')

out = {}

with open('../samples/earbuds_B000I68BD4_(N=1018_Stdev=1.34810039761).csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter = ',')
	for row in csvreader:
		doc = nlp(row[4])
		amod = []
		compound = []
		for token in doc:
			if token.dep_ == 'compound':
				compound.append((token.text, token.head.text));
			elif token.dep_ == 'amod':
				amod.append(token.text)
		out[row[4]] = {'amods': amod, 'compounds': compound}

	pickle.dump(out, open('earbuds.pkl', 'wb'))
	print (out)