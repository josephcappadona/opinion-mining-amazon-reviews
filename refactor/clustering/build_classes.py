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

    if len(args) != 5:
        print('USAGE:  python build_classes.py WORD2VEC_PATH CORPUS.txt OUTPUT.txt W2V_CONFIG.yaml')
    word2vec_path = args[1]
    corpus_filepath = args[2]
    output_filepath = args[3]
    config_filepath = args[4]

    word2vec_args = parse_config(config_filepath)
    os.system('%s -train %s -output %s %s' % (word2vec_path, corpus_filepath, output_filepath, word2vec_args))
