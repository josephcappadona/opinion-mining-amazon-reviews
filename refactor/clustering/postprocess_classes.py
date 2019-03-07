from collections import defaultdict

def build_data_structures(classes_filepath):

    word_to_class_id = {}
    class_id_to_words = defaultdict(list)
    with open(classes_filepath, 'rt') as classes_file:
        for line in classes_file:
            word, class_id = line.split()
            word_to_class_id[word] = class_id
            class_id_to_words[class_id].append(word)
    return word_to_class_id, class_id_to_words

