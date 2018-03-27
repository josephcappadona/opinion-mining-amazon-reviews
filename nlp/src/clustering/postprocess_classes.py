import pickle

classes_file = open("./results/classes.sorted.txt", "r")
output_file = open("./results/classes.pkl", "wb")

word_to_class = dict()

for line in classes_file:
	parts = line.split()
	if len(parts) != 2:
		continue
	word = parts[0]
	class_num = int(parts[1])
	word_to_class[word] = class_num
	#print("Adding " + word + " to class " + str(class_num))

pickle.dump(word_to_class, output_file, -1)

classes_file.close()
output_file.close()
