#!/bin/bash

#$ -o ../../../output/dispatch_corenlp_{0}.out
#$ -e ../../../output/dispatch_corenlp_{0}.err
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

python corenlp.py {1} {2} {3} {4}

echo "Finish - "
/bin/date

echo $1
