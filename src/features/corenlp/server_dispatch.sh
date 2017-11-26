#!/bin/bash

#$ -o ./output/server_dispatch.out
#$ -e ./output/server_dispatch.err
#$ -l h_rt=01:00:00
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

java -mx4g -cp "../../../CoreNLP/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

echo "Started CoreNLP server"
