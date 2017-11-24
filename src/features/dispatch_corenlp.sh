#!/bin/bash

#$ -o ../output/dispatch_corenlp.out
#$ -e ../output/dispatch_corenlp.err
#$ -l h_rt=00:30:00
#$ -l 'arch=*64*'
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -M jcapp@seas.upenn.edu
#$ -m e

# when am I running
echo "Start - "
/bin/date

# where am I running
/bin/hostname

# what environment variables are available to this job script, e.g. $JOB_ID
/usr/bin/env

source ../virtualenv/bin/activate

python corenlp.py ../data/reviews_Cell_Phones_and_Accessories_5.json ../results/ 50 0

echo "Finish - "
/bin/date

echo $1
