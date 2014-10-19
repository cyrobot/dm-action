#-coding-: utf-8 -*-
__author__ = 'robert'

def dict_print(dic):
    print '{'
    for k in dic:
        print k, ':', dic[k]
    print '}'

def dict_append(dic, k, v):
    if k not in dic:
        dic[k] = v

def list_print(lst):
    print '['
    for l in lst:
        print l
    print ']'
