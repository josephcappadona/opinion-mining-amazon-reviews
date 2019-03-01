from collections import defaultdict

def build_data_structures(clusters_filepath):

    word_to_cluster_id = {}
    cluster_id_to_words = defaultdict(list)
    with open(clusters_filepath, 'rt') as clusters_file:
        for line in clusters_file:
            word, cluster_id = line.split()
            word_to_cluster_id[word] = cluster_id
            cluster_id_to_words[cluster_id].append(word)
    return word_to_cluster_id, cluster_id_to_words

