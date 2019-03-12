wget https://storage.googleapis.com/google-code-archive-source/v2/code.google.com/word2vec/source-archive.zip

unzip source-archive.zip
rm source-archive.zip

mv word2vec/trunk/* word2vec/
rm -rf word2vec/trunk

cd word2vec
make
cd ..

echo "\nword2vec executable located at './word2vec/word2vec'"
