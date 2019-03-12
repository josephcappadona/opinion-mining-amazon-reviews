
### Example
```
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
unzip stanford-corenlp-full-2018-10-05.zip; rm stanford-corenlp-full-2018-10-05.zip

cp ../word2vec/electronics_servers_reviews.json .

java -mx4g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
python test.py electronics_servers_reviews.json
```
