#!/bin/bash

#$ -o ../../../output/dispatch_corenlp_18.out
#$ -e ../../../output/dispatch_corenlp_18.err
#$ -l h_rt=01:00:00
#$ -l mem=16G
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -M jcapp@seas.upenn.edu
#$ -m ae

# when am I running
echo "Start - "
/bin/date

# where am I running
/bin/hostname

# what environment variables are available to this job script, e.g. $JOB_ID
/usr/bin/env

source ../../../virtualenv/bin/activate

python corenlp.py ../../../data/reviews_Cell_Phones_and_Accessories_5.json ../../../results/ 500 9000

echo "Finish - "
/bin/date

echo $1
