For extended instructions, see [NLPGrid Usage Guide](https://docs.google.com/document/d/1xQ9RRSatez7NBTDc-bxbrNKnnvB-fZbB292e90L_ZJY/edit)

# Setup

`ssh pennkey@nlpgrid.seas.upenn.edu`

`cd ~/path/to/dir/senior-design-f17/src/features`

`mkdir ../../../results/`

`mkdir ../../../output/`

`mkdir ../../../virtualenv/`


# Creating dispatch files
To create dispatch scripts, use the `make_corenlp_dispatch.py`:
  
  Usage: `python make_corenlp_dispatch.py template_file.sh data_file.json job_results_dir interval num_jobs script_output_dir [skip]`

    `template_file.sh` = job dispatch template file
    `data_file.json` = path to data file to process
    `job_results_dir` = path to results of processing
    `interval` = num of data points to be processed per job
    `num_jobs` = num of jobs (total data points = interval * num\_jobs)
    `output_dir` = dispatch script output directory
    `skip` (optional) = num of data points to skip (if not starting from beginning of data file)


`make_corenlp_dispatch.py` works by inserting job parameters into the template file.

For example,

`python make_corenlp_dispatch.py corenlp_dispatch_template.sh ../../../data/reviews_Cell_Phones_and_Accessories_5.json ../../../results/ 500 20 ./corenlp 0`

This will make 20 dispatch files in the directory `./corenlp` named `dispatch_0.sh` through `dispatch_19.sh`, the first processing data points [0,499], the second [500,999], the third, [1000,1499], etc, for a total of 10000 data points.


# Launching jobs
`for i in {0..9}; do qsub ./corenlp/dispatch_$i.sh; done`

I would recommend launching them in small batches (<10) at a time so they don't get delegated to the same grid node. Not sure why this is necessary, but it helps. I'm not sure the job parameters are optimized, feel free to play with the `-l mem` parameter within `corenlp_dispatch_template.py`. You'll also want to modify the parameters `-o`, `-e`, `-l h_rt`, `-M`, `-m` to suit your needs. See NLPGrid Usage Guide above for full details.

To monitor jobs,
    `qstat | grep pennkey`

Results will be timestamped in `../../../results`.

# Full example

```
ssh jcapp@nlpgrid.seas.upenn.edu
cd ~/Documents/SeniorDesign/senior-design-f17/src/features
ls ../../../results
ls ../../../data
rm ../../../output/*

mkdir ./corenlp
python make_corenlp_dispatch.py corenlp_dispatch_template.sh ../../../data/reviews_Cell_Phones_and_Accessories_5.json ../../../results/ 500 20 ./corenlp 0

for i in {0..9}; do qsub ./corenlp/dispatch_$i.sh; done
for i in {10..19}; do qsub ./corenlp/dispatch_$i.sh; done

qstat | grep jcapp

tail -f ../../../output/dispatch_corenlp_0.err
tail -f ../../../output/dispatch_corenlp_0.out

ls ../../../results

```
