__author__ = 'robert'

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
