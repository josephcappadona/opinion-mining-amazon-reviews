time ./word2vec/word2vec -train ./results/reviews_data_word2vec.txt -output ./results/classes.txt -cbow 1 -size 300 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -min-count 100 -debug 2 -classes 500
sort ./results/classes.txt -k 2 -n > ./results/classes.sorted.txt
echo The word classes were saved to file classes.sorted.txt
