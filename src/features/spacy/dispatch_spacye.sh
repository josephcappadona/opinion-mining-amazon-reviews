#!/bin/bash

#$ -o ../output/dispatch.out
#$ -e ../output/dispatch.err
#$ -l 'arch=*64*'
#$ -S /bin/bash
#$ -cwd
#$ -V
#$ -M jcapp@seas.upenn.edu
#$ -m eab

# when am I running
echo "Start - "
/bin/date

# where am I running
/bin/hostname

# what environment variables are available to this job script, e.g. $JOB_ID
/usr/bin/env

source ../virtualenv/bin/activate

python spacye.py ../data/reviews_Cell_Phones_and_Accessories_5.json ../results/

echo "Finish - "
/bin/date

