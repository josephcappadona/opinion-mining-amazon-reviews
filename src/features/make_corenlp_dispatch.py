import sys

if len(sys.argv) < 7:
  print "Usage: python make_dispatch.py template_file.py data_file.json job_output_dir interval num_jobs script_output_dir [skip]"
  exit()

template_file = sys.argv[1]
data_file = sys.argv[2] # data file to process
job_output_dir = sys.argv[3] # path to results of processing
interval = int(sys.argv[4]) # num of data points per job
num_jobs = int(sys.argv[5]) # num of jobs
script_output_dir = sys.argv[6] # dispatch script output directory
skip = int(sys.argv[7]) if len(sys.argv) >= 8 else 0 # num of data points to skip (if not starting from beginning of data file)

# open template
template = open(template_file)
text = template.read()

# create new file contents from template
l = []
for i in range(num_jobs):
  l.append(text.format(i, data_file, job_output_dir, interval, interval * i + skip))

# write new dispatch files
for i in range(num_jobs):
  new_f = open(script_output_dir + "/" + "dispatch_{}.sh".format(i), "w+")
  new_f.write(l[i])
  new_f.close()

