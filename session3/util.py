#-*-coding: utf-8 -*-
__author__ = 'robert'

FP_POSITIVE_ASEEDS = 'abstracted_positive.seed'
FP_NEGATIVE_ASEEDS = 'abstracted_negative.seed'
FP_PROPERTIES_FILE = 'properties.sav'
FP_RECORD_FILE = ['kongtiao.segment']

ENGLISH_BREAKPOINTS = '!@#$%^&*()[]{}/.,;?<>""'
CHINESE_BREAKPOINTS = '！@#￥%……&×（）{}【】？《》；。“”，'

PROPERTY_THRESHOLD = 10
POSITIVE_THRESHOLD = 20
NEGATIVE_THRESHOLD = 5

NEGATIVE_ATTITUDE = -1
POSITIVE_ATTITUDE = 1
NONE_ATTITUDE = 0

def print_list(lst, desc):
    print desc, ": [",
    for item in lst:
        print '$', item,
    print ']'

def print_dict(dic, desc):
    print desc, ": {",
    for k in dic:
        print '$', k, ':', dic[k],
    print '}'

def append_dict(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

def sort_dict(dic):
    return sorted(dic.iteritems(), key = lambda v:v[1], reverse=True)

def load_dict_file(file_path):
    dic = {}
    fp = open(file_path)
    for line in fp:
        line = line.strip('\n')
        k, v = line.split('\t')
        dic[k] = v
    fp.close()
    return dic

def combine_seed(pos, v, vocab, vocabp):
    while pos >= 1:
        if vocabp[pos-1] == 'd':
            v = vocab[pos-1] + v
        else:
            break
        pos -= 1
    return v

def judge_attitude(vocab,vocabp, positive_seeds, negative_seeds):
    positive_count = 0
    negative_count = 0
    for pos, v in enumerate(vocab):
        combine_seed(pos, v, vocab, vocabp)
        if v in positive_seeds:
             positive_count += 1
        elif v in negative_seeds:
            negative_count += 1
    if positive_count > 1 and negative_count == 0:
            return POSITIVE_ATTITUDE
    elif positive_count == 0 and negative_count > 0:
            return NEGATIVE_ATTITUDE
    return NONE_ATTITUDE
