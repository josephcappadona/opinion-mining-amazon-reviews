## Feature Extraction Pipeline
### Files
`corenlp_sandbox.py`: Annotates the reviews with CoreNLP (NLTK wrapper), then extracts all noun phrase, modifier pairs for each review.
  - Pickle format: `list((asin, dict(phrase -> [adjs])))`

`corenlp_sandbox_dispatch_template.py`: Creates the dispatch scripts.

`./corenlp/server_dispatch.sh`: Starts a CoreNLP server on port 9000.

`process_nlp_results.py`: With pickle from the sandbox, aggregates by product. Right now, it removes features that aren't in a minimum % of all reviews for that product and then sorts by # of adjs for that feature.
  - Pickle format: `dict(asin -> list((phrase, [adjs])))`

`check_sandbox_pickle.py`: Prints the sandbox pickle and the # reviews processed.

`check_process_pickle.py`: Prints the process pickle and the # products and # reviews processed.

Job error and standard output go in `./output`, pickles go in `./results`, dispatch files go in `./corenlp`. Make sure CoreNLP is installed in `../../../CoreNLP`.

### Steps
1. Make `corenlp_sandbox` dispatch scripts
  - `python make_corenlp_dispatch.py corenlp_sandbox_dispatch_template.sh {filepath to data} ./results {# reviews / job} {# jobs} ./corenlp`.
2. Submit jobs
  - `qsub ./corenlp/server_dispatch.sh; for i in {0..x}; do qsub ./corenlp/dispatch_$i.py; done`
  - We need to submit a separate job that starts up the CoreNLP server. It must be submitted to the same node as the actual jobs, but this should happen as long as you submit in a single batch.
3. Monitor jobs
  - `tail -f ./output/dispatch_corenlp_sandbox_0.err`
4. Check the resulting pickle
  - `python check_sandbox_pickle.py ./results/{file}.pickle`
5. Create a file with the filenames (not paths) of each result pickle.
  - `ls ./results > fns.txt`
5. Run the processing script
  - `python process_nlp_results.py fns.txt`
6. Check the resulting pickle
  - `python check_process_pickle.py ./results/features.pickle`

### Known bugs
* NLTK parsing fails for certain reviews and throws an error that aborts the sandbox script (need to look into).
* Submitting a separate job for starting the server is a bit hacky (low priority).

## Guide to NLPGrid
For extended instructions, see [NLPGrid Usage Guide](https://docs.google.com/document/d/1xQ9RRSatez7NBTDc-bxbrNKnnvB-fZbB292e90L_ZJY/edit)

### Setup

`ssh pennkey@nlpgrid.seas.upenn.edu`

`cd ~/path/to/dir/senior-design-f17/src/features`

`mkdir ./results/`

`mkdir ./output/`

`mkdir ../../../virtualenv/`

`mkdir ../../../CoreNLP/`


### Creating dispatch files
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

`python make_corenlp_dispatch.py corenlp_dispatch_template.sh ../../../data/reviews_Cell_Phones_and_Accessories_5.json ./results/ 500 20 ./corenlp 0`

This will make 20 dispatch files in the directory `./corenlp` named `dispatch_0.sh` through `dispatch_19.sh`, the first processing data points [0,499], the second [500,999], the third, [1000,1499], etc, for a total of 10000 data points.


### Launching jobs
`for i in {0..9}; do qsub ./corenlp/dispatch_$i.sh; done`

I would recommend launching them in small batches (<10) at a time so they don't get delegated to the same grid node. Not sure why this is necessary, but it helps. I'm not sure the job parameters are optimized, feel free to play with the `-l mem` parameter within `corenlp_dispatch_template.py`. You'll also want to modify the parameters `-o`, `-e`, `-l h_rt`, `-M`, `-m` to suit your needs. See NLPGrid Usage Guide above for full details.

To monitor jobs,
    `qstat | grep pennkey`

Results will be timestamped in `../../../results`.

### Full example

```
ssh jcapp@nlpgrid.seas.upenn.edu
cd ~/Documents/SeniorDesign/senior-design-f17/src/features
ls ./results
ls ../../../data
rm ./output/*

mkdir ./corenlp
python make_corenlp_dispatch.py corenlp_dispatch_template.sh ../../../data/reviews_Cell_Phones_and_Accessories_5.json ./results/ 500 20 ./corenlp 0

for i in {0..9}; do qsub ./corenlp/dispatch_$i.sh; done
for i in {10..19}; do qsub ./corenlp/dispatch_$i.sh; done

qstat | grep jcapp

tail -f ./output/dispatch_corenlp_0.err
tail -f ./output/dispatch_corenlp_0.out

ls ./results

```
