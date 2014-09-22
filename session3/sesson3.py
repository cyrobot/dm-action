#-*-coding: utf-8 -*-
__author__ = 'robert'

from util import *

# comments analyze

# global resources
FP_NEGATIVE_SEEDS = 'negative.seed'
FP_POSITIVE_SEEDS = 'positive.seed'

PROPERTIES_FILTER_WORDS = ['有点']

# seed list
negative_seeds = []
positive_seeds = []
good_properties = {}
evaluation = {}
new_positive_seeds = {}
new_negative_seeds = {}
positive_comment_count = 0
negative_comment_count = 0
positive_comments = {}
negative_comments = {}

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
        append_dict(good_properties, k)

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

def append_comments(comments, new_comment):
    for c in new_comment:
        append_dict(comments, c)

def find_seed(start, vocab, vocabp, v):
    new_seed = None
    comment = None
    if (start >= len(vocab)):
        return None, None
    for cursor in xrange(start, len(vocab)):
        if vocab[cursor] in ENGLISH_BREAKPOINTS:
            break
        if vocab[cursor] in CHINESE_BREAKPOINTS:
            break
        if vocabp[cursor] == 'n':
            break
        if vocabp[cursor] == 'a':
            # new_seed = combine_seed(cursor, vocab[cursor], vocab, vocabp)
            new_seed = vocab[cursor]
            comment = v + new_seed
            break
    return new_seed, comment

def append_seeds(lst, new_seeds):
    for seed in new_seeds:
        append_dict(lst, seed)

def mining_seeds(vocab, vocabp, properties):
    global positive_comment_count
    global negative_comment_count
    new_seeds = {}
    valid_comments = {}
    if vocab is None:
        return
    for pos, v in enumerate(vocab):
        if v in properties:
            new_seed, comment = find_seed(pos+1, vocab, vocabp, v)
            if new_seed is not None:
                new_seeds[new_seed] = 1
                append_dict(valid_comments, comment)
    if len(new_seeds) == 0:
        return
    attitude = judge_attitude(vocab, vocabp, positive_seeds, negative_seeds)
    if attitude == POSITIVE_ATTITUDE:
        append_seeds(new_positive_seeds, new_seeds)
        positive_comment_count += 1
        append_comments(positive_comments, valid_comments)
    elif attitude == NEGATIVE_ATTITUDE:
        append_seeds(new_negative_seeds, new_seeds)
        negative_comment_count += 1
        append_comments(negative_comments, valid_comments)
    print '----------------------------------------'
    print_dict(new_seeds, "New seeds")
    display_state()

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

def parse_comment_line1(comment, properties):
    # id, user, comment
    comment = comment.strip('\n')
    items = comment.split('\t')
    if len(items) < 3:
        return
    good_id = items[0]
    user = items[1]
    vocab = items[2::2]
    vocabp = items[3::2]
    mining_seeds(vocab, vocabp, properties)

def filter_properties():
    new_good_properties = {}
    for k in good_properties:
        if k in PROPERTIES_FILTER_WORDS:
            continue
        if good_properties[k] >= PROPERTY_THRESHOLD:
            new_good_properties[k] = good_properties[k]
    return new_good_properties

def filter_seeds(seeds, threshold):
    """
    filter the positive/negative seeds with threshold
    :param seeds: positive/negative seeds, dict type
    :param threshold: int
    :return: seeds dict
    """
    new_seeds = {}
    for k in seeds:
        if seeds[k] > threshold:
            new_seeds[k] = seeds[k]
    return new_seeds

def parse_record_file(filepath, sample_count):
    fp = open(filepath)
    for i, comment in enumerate(fp):
        parse_comment_line0(comment)
        if sample_count > 0 and i >= sample_count:
            break
    fp.close()
    good_properties = filter_properties()
    fp = open(filepath)
    for i, comment in enumerate(fp):
        # if i > 9000:
        #     break
        parse_comment_line1(comment, good_properties)
    fp.close()
    abstracted_positive_seeds = filter_seeds(new_positive_seeds, POSITIVE_THRESHOLD)
    abstracted_negative_seeds = filter_seeds(new_negative_seeds, NEGATIVE_THRESHOLD)
    display_result(good_properties, abstracted_positive_seeds, abstracted_negative_seeds)
    save_abstracted_properties(good_properties, FP_PROPERTIES_FILE)
    save_seeds(abstracted_positive_seeds, FP_POSITIVE_ASEEDS, positive_seeds)
    save_seeds(abstracted_negative_seeds, FP_NEGATIVE_ASEEDS, negative_seeds)

def save_abstracted_properties(properties, file_path):
    fp = open(file_path, 'w')
    sorted_properties = sort_dict(properties)
    for k, v in sorted_properties:
        pstr = k + '\t' + str(v) + '\n'
        fp.write(pstr)
    fp.close()

def save_seeds(seeds, file_path, origin):
    fp = open(file_path, 'w')
    sorted_seeds = sort_dict(seeds)
    first = True
    for k, v in sorted_seeds:
        if first:
            for o in origin:
                if o not in seeds:
                    pstr = o + '\t' + str(v) + '\n'
                    fp.write(pstr)
            first = False
        pstr = k + '\t' + str(v) + '\n'
        fp.write(pstr)
    fp.close()

def display_result(properties, positive, negative):
    print '******************************************'
    print 'Result: '
    print_dict(properties, 'Properties')
    print_dict(positive, 'Positive seeds')
    print_dict(negative, 'Negative seeds')

def display_comments():
    print 'Positive comments: {',
    for k in positive_comments:
        if positive_comments[k] > POSITIVE_THRESHOLD:
            print k, ':', positive_comments[k],
    print '}'
    print 'Negative comments: {',
    for k in negative_comments:
        if negative_comments[k] > NEGATIVE_THRESHOLD:
            print k, ':', negative_comments[k],
    print '}'

def display_state():
    print 'positive count:', positive_comment_count
    print 'negative count:', negative_comment_count
    print_dict(new_positive_seeds, 'New positive seeds')
    print_dict(new_negative_seeds, 'New negative seeds')
    display_comments()

if __name__ == "__main__":
    print 'Start demo:'
    negative_seeds = load_seed(FP_NEGATIVE_SEEDS)
    positive_seeds = load_seed(FP_POSITIVE_SEEDS)
    display_state()
    for f in FP_RECORD_FILE:
        parse_record_file(f, -1)
