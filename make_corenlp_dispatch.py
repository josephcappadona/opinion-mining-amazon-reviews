import sys

if len(sys.argv) < 5:
  print "Usage: python make_dispatch.py template_file.py interval num_files output_dir"
  exit()

template_file = sys.argv[1]
interval = int(sys.argv[2])
num_files = int(sys.argv[3])
output_dir = sys.argv[4]

# open template
template = open(template_file)
text = template.read()

# create new file contents from template
l = []
for i in range(num_files):
  l.append(text.format(i, interval, interval * i))

# write new dispatch files
for i in range(num_files):
  new_f = open(output_dir + "/" + "dispatch_{}.sh".format(i), "w+")
  new_f.write(l[i])
  new_f.close()

