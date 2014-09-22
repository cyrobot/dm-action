#-*-coding: utf-8 -*-

__author__ = 'robert'

from util import *

# 3 files storing properties, positive/negative files

goods_properties = {}
positive_vocabs = {}
negative_vocabs = {}
attitude_vocabs = []
goods_tags = {}

def display_tags():
    global goods_tags

    print 'Tags: {',
    for id in goods_tags:
        print '*', id, ': [',
        if goods_tags[id][0] is None:
            print 'None, ',
        else:
            print '{',
            for comment in goods_tags[id][0]:
                print '**', comment, ':', goods_tags[id][0][comment],
            print '}, ',
        if goods_tags[id][1] is None:
            print 'None',
        else:
            print '{',
            for comment in goods_tags[id][1]:
                print '**', comment, ":", goods_tags[id][1][comment],
            print '}',
        print ']'
    print '}'

def save_tags(file_path):
    global goods_tags

    fp = open(file_path, 'w')
    for id in goods_tags:
        pstr = '------------------------------'
        fp.write(pstr)
        pstr = "Goods ID: " + id + '\n'
        fp.write(pstr)
        pstr = '正面评价:\n'
        fp.write(pstr)
        if goods_tags[id][0] is None:
            pstr = '\t无\n'
            fp.write(pstr)
        else:
            for comment in goods_tags[id][0]:
                pstr = '\t' + comment + ": " + str(goods_tags[id][0][comment]) + '\n'
                fp.write(pstr)

        pstr = '负面评价:\n'
        fp.write(pstr)
        if goods_tags[id][1] is None:
            pstr = '\t无\n'
            fp.write(pstr)
        else:
            for comment in goods_tags[id][1]:
                pstr = '\t' + comment + ": " + str(goods_tags[id][1][comment]) + '\n'
                fp.write(pstr)
        fp.write('\n')
    fp.close()

def test_display_tags():
    global goods_tags
    goods_tags = {'a': [{'b': 1}, {'c': 2}], 'd': [{'e' : 3}, {'f' : 4}]}
    display_tags()

def load_eval_tags():
    global goods_properties, positive_vocabs, negative_vocabs, attitude_vocabs
    goods_properties = load_dict_file(FP_PROPERTIES_FILE)
    positive_vocabs = load_dict_file(FP_POSITIVE_ASEEDS)
    negative_vocabs = load_dict_file(FP_NEGATIVE_ASEEDS)
    attitude_vocabs = set([k for k in positive_vocabs]).union([k for k in negative_vocabs])
    print_list(attitude_vocabs, 'Attitude')
    print_dict(goods_properties, 'Goods properties')
    print_dict(positive_vocabs, 'Positive vocabs')
    print_dict(negative_vocabs, 'Negative vocabs')

def find_properties(pos, vocab, vocabp):
    comment = ''
    prop = None
    while pos >= 0:
        if vocabp[pos] == 'x':
            break
        if vocabp[pos] == 'n':
            prop = vocab[pos]
            comment = prop + comment
            break
        if vocabp[pos] != 'd':
            break
        pos -= 1

    return prop, comment

def append_comments(id, comments, attitude):
    global goods_tags

    if len(comments) == 0:
        return

    if id in goods_tags:
        if attitude == POSITIVE_ATTITUDE:
            if goods_tags[id][0] is None:
                goods_tags[id][0] = comments.copy()
            else:
                for k in comments:
                    append_dict(goods_tags[id][0], k)
        elif attitude == NEGATIVE_ATTITUDE:
            if goods_tags[id][1] is None:
                goods_tags[id][1] = comments.copy()
            else:
                for k in comments:
                    append_dict(goods_tags[id][1], k)
    else:
        if attitude == POSITIVE_ATTITUDE:
            goods_tags[id] = [comments.copy(), None]
        elif attitude == NEGATIVE_ATTITUDE:
            goods_tags[id] = [None, comments.copy()]

def evaluation(vocab, vocabp):
    global attitude_vocabs
    global positive_vocabs, negative_vocabs
    global  positive_comments, negative_comments
    comments = {}
    for pos, v in enumerate(vocab):
        if v in attitude_vocabs:
            prop, comment = find_properties(pos-1, vocab, vocabp)
            if prop is not None and prop in goods_properties:
                comment = prop + v
                comments[comment] = 1
    print_list(vocab, 'Vocab')
    print_dict(comments, "Comments")
    attitude = judge_attitude(vocab, vocabp, positive_vocabs, negative_vocabs)
    return attitude, comments

def eval_comment(comment):
    items = comment.split('\t')
    if len(items) < 3:
        return
    good_id = items[0]
    vocab = items[2:-1:2]
    vocabp = items[3:-1:2]
    attitude, comments = evaluation(vocab, vocabp)
    append_comments(good_id, comments, attitude)
    # display_tags()

def parse_data_file(file_path):
    fp = open(file_path)
    for i, comment in enumerate(fp):
        # if i > 1000:
        #     break
        comment = comment.strip('\n')
        eval_comment(comment)
    fp.close()

if __name__ == '__main__':
    load_eval_tags()
    # test_display_tags()
    # parse_data_file('test.segment')
    for i, f in enumerate(FP_RECORD_FILE):
        parse_data_file(f)
        save_tags('result-'+ str(i) + '.txt')
