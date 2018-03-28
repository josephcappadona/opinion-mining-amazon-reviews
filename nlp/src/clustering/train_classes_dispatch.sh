#!/bin/bash

#$ -o ./output/train_classes.out
#$ -e ./output/train_classes.err
#$ -l h_rt=12:00:00
#$ -l mem=16G
#$ -S /bin/bash
#$ -cwd
#$ -pe parallel-onenode 20
#$ -V
#$ -M carzheng@seas.upenn.edu
#$ -m ae

# when am I running
echo "Start - "
/bin/date

# where am I running
/bin/hostname

# what environment variables are available to this job script, e.g. $JOB_ID
/usr/bin/env

source ../../../../virtualenv/bin/activate

#(
#java -mx4g -cp "../../../CoreNLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
#)&
#echo "Started CoreNLP server"
#python corenlp_sandbox.py {1} {2} {3} {4}
time ./word2vec/word2vec -train ./results/reviews_data_word2vec.txt -output ./results/classes.txt -cbow 1 -size 300 -window 8 -negative 25 -hs 0 -sample 1e-4 -threads 20 -iter 15 -min-count 100 -debug 2 -classes 500
sort ./results/classes.txt -k 2 -n > ./results/classes.sorted.txt
echo The word classes were saved to file classes.sorted.txt

echo "Finish - "
/bin/date

echo $1
