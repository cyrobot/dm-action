#-*-coding: utf-8 -*-
__author__ = 'robert'

import string

from session1.util import *


DATA_FILE = 'data/sohu_news_data'
DELESTR= string.punctuation + ' ' + string.digits
DELCSTR = '《》（）&%￥#@！{}【】，。“”、.,;；．[]…'

def find_terms_in_doc(doc):
    """
    preprocessing terms in documents
    """
    doc = doc.strip(' ')
    doc = doc.strip('\n')
    terms_in_doc = doc.split()
    print_list(terms_in_doc)
    terms = []
    for term in terms_in_doc:
        if term is None:
            continue
        if term in DELESTR:
            continue
        if term in DELCSTR:
            continue
        if term == '\xe3\x80\x80':
            continue
        terms.append(term)
    return terms[0], terms[1:]

def add_doc_terms(term_dict, doc_class, doc_terms):
    if doc_class in term_dict:
        term_dict[doc_class].append(doc_terms)
    else:
        term_dict[doc_class] = [doc_terms]

def extract_terms():
    """
    extract term frequency for each document.
    """
    data_fd = open(DATA_FILE)
    term_dict = {}
    for i, doc in enumerate(data_fd):
        doc_class, terms = find_terms_in_doc(doc)
        add_doc_terms(term_dict, doc_class, terms)
        print_list(terms)
        if i == 2:
            return
    data_fd.close()

def test():
    print 'Extract term frequency...'
    extract_terms()


if __name__ == "__main__":
    test()
