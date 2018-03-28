#!/bin/bash

#$ -o ./output/preprocess_reviews.out
#$ -e ./output/preprocess_reviews.err
#$ -l h_rt=05:00:00
#$ -l mem=16G
#$ -S /bin/bash
#$ -cwd
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

source ../../../virtualenv/bin/activate

#(
#java -mx4g -cp "../../../CoreNLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
#)&
#echo "Started CoreNLP server"
#python corenlp_sandbox.py {1} {2} {3} {4}
python preprocess_reviews2.py

echo "Finish - "
/bin/date

echo $1
