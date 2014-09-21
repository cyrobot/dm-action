#-*-coding: utf-8 -*-
__author__ = 'robert'

from util import *

# comments analyze

# global resources
FP_NEGATIVE_SEEDS = 'negative.seed'
FP_POSITIVE_SEEDS = 'positive.seed'
FP_RECORD_FILE = ['kongtiao.segment']
PROPERTY_THRESHOLD = 5
ENGLISH_BREAKPOINTS = '!@#$%^&*()[]{}/.,;?<>""'
CHINESE_BREAKPOINTS = '！@#￥%……&×（）{}【】？《》；。“”'
NEGATIVE_ATTITUDE = -1
POSITIVE_ATTITUDE = 1
NONE_ATTITUDE = 0

# seed list
negative_seeds = []
positive_seeds = []
good_properties = {}
evaluation = {}
new_positive_seeds = {}
new_negative_seeds = {}

def load_seed(filepath):
    # load seeds from file
    fp = open(filepath)
    seeds = []
    for seed in fp:
        seed = seed.rstrip('\n')
        seeds.append(seed)
    fp.close()
    return seeds

def add_good_properties(dic):
    for k in dic:
        append_properties(good_properties, k)

def mining_properties(vocab, vocabp):
    seeds = set(negative_seeds).union(set(positive_seeds))
    properties_dict = {}
    for pos, v in enumerate(vocab):
        if v in seeds:
            if pos > 0:
                prop_pos = pos - 1
                judge = v
                if vocabp[prop_pos] == 'd':
                    judge = vocab[prop_pos] + judge
                    prop_pos -= 1
                if prop_pos >= 0 and vocabp[prop_pos] == 'n':
                    properties_dict[vocab[prop_pos]] = 1
    add_good_properties(properties_dict)


def find_seed(start, vocab, vocabp):
    new_seed = None
    if (start >= len(vocab)):
        return None
    for cursor in xrange(start, len(vocab)):
        if vocab[cursor] in ENGLISH_BREAKPOINTS:
            break
        if vocab[cursor] in CHINESE_BREAKPOINTS:
            break
        if vocabp[cursor] == 'a':
            new_seed = vocab[cursor]
            break
    return new_seed

def check_attitude(vocab):
    positive_count = 0
    negative_count = 0
    for v in vocab:
        if v in positive_seeds:
             positive_count += 1
        elif v in negative_seeds:
            negative_count += 1
    if positive_count > 1 and negative_count == 0:
            return POSITIVE_ATTITUDE
    elif positive_count == 0 and negative_count > 1:
            return NEGATIVE_ATTITUDE
    return NONE_ATTITUDE

def append_seeds(lst, new_seeds):
    for seed in new_seeds:
        if seed not in lst:
            lst.append(seed)

def mining_seeds(vocab, vocabp):
    new_seeds = {}
    for pos, v in enumerate(vocab):
        if v in good_properties:
            new_seed = find_seed(pos+1, vocab, vocabp)
            if new_seed is not None:
                new_seeds[new_seed] = 1
    attitude = check_attitude(vocab)
    if attitude == POSITIVE_ATTITUDE:
        print_list(vocab, "Vocab")
        append_seeds(positive_seeds, new_seeds)
    elif attitude == NEGATIVE_ATTITUDE:
        print_list(vocab, "Vocab")
        append_seeds(negative_seeds, new_seeds)
    display_state()
    print_dict(new_seeds, "New seeds")

def parse_comment_line0(comment):
    # id, user, comment
    comment = comment.strip('\n')
    items = comment.split('\t')
    if len(items) < 3:
        return
    good_id = items[0]
    user = items[1]
    vocab = items[2:-1:2]
    vocabp = items[3:-1:2]
    mining_properties(vocab, vocabp)

def parse_comment_line1(comment):
    # id, user, comment
    comment = comment.strip('\n')
    items = comment.split('\t')
    if len(items) < 3:
        return
    good_id = items[0]
    user = items[1]
    vocab = items[2::2]
    vocabp = items[3::2]
    # print_list(vocab, "Vocab")
    # print_list(vocabp, 'Vocabp')
    mining_seeds(vocab, vocabp)

def filter_properties():
    new_good_properties = {}
    for k in good_properties:
        if good_properties[k] >= PROPERTY_THRESHOLD:
            new_good_properties[k] = good_properties[k]
    return new_good_properties

def parse_record_file(filepath, sample_count):
    fp = open(filepath)
    for i, comment in enumerate(fp):
        parse_comment_line0(comment)
        if sample_count > 0 and i >= sample_count:
            break
    fp.close()
    good_properties = filter_properties()
    print_dict(good_properties, 'Good properties')
    fp = open(filepath)
    for i, comment in enumerate(fp):
        if i > 500:
            break
        parse_comment_line1(comment)
    fp.close()

def display_state():
    print_list(negative_seeds, "Negative seeds")
    print_list(positive_seeds, "Positive seeds")

if __name__ == "__main__":
    print 'Start demo:'
    negative_seeds = load_seed(FP_NEGATIVE_SEEDS)
    positive_seeds = load_seed(FP_POSITIVE_SEEDS)
    display_state()
    for f in FP_RECORD_FILE:
        parse_record_file(f, 1500)
