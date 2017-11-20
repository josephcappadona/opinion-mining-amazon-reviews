import spacy
nlp = spacy.load('en')
doc = nlp(u'The poor battery life.')
for token in doc:
	if token.dep_ == 'compound':
		print ("compound")
		print (token.text, token.head.text)
	elif token.dep_ == 'amod':
		print ("amod")
		print (token.text)