from sys import argv as args
import os
import yaml

def parse_config(config_filepath):
    w2v_args_string = ''
    with open(config_filepath, 'rt') as config_file:
        w2v_args = yaml.load(config_file)
        for arg_name, arg in w2v_args.items():
            w2v_args_string += '-%s %s ' % (arg_name, arg)
    return w2v_args_string

if __name__ == '__main__':

    if len(args) != 4:
        print('USAGE:  python build_clusters.py CORPUS_FILEPATH.txt OUTPUT_FILEPATH.txt CONFIG_FILEPATH.yaml')
    corpus_filepath = args[1]
    output_filepath = args[2]
    config_filepath = args[3]

    word2vec_args = parse_config(config_filepath)
    os.system('../../../word2vec/word2vec -train %s -output %s %s' % (corpus_filepath, output_filepath, word2vec_args))
