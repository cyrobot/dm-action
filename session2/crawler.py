#-*-coding: utf-8 -*-
__author__ = 'robert'

import urllib2
import os
import BeautifulSoup as bs
import scrapy

JD_FOOD_LINK_PREFIX = u"http://list.jd.com/list.html?cat=1320%2C1583%2C1590&page="
JD_FOOD_LINK_POSTFIX = u"&JL=6_0_0"

FP_ITEM_INFO_LIST = u'data/items_info.txt'

def get_page(urlstr):
    """
    get page content
    """
    content = urllib2.urlopen(urlstr).read();
    return content

def store_page(content, filepath):
    if os.path.exists(filepath):
        return
    fp = open(filepath, 'w')
    fp.write(content)
    fp.close()

def restore_page(filepath):
    content = None
    if os.path.exists(filepath):
        fp = open(filepath)
        content = fp.read(100000)
        fp.close()
    return content

def get_next_page_url(cur_page_no):
    """
    check whether if next page and retrieve it
    """
    url = JD_FOOD_LINK_PREFIX + str(cur_page_no + 1) + JD_FOOD_LINK_POSTFIX

    # check if has next page
    content = get_page(url)
    soup = bs.BeautifulSoup(content)
    list = soup.findAll('span', {'class': 'next-disabled'})
    if len(list) == 0:
        return url
    return None

def store_item_link_info(info_str, path):
    fp = open(path, 'a')
    # fp.writelines(info_str)
    fp.write(info_str)
    fp.close()

def check_file_exits(file_path):
    """
    check the file whether if existing
    """
    if os.path.exists(os.path.realpath(file_path)):
        return True
    return False

def analyze_url_list():
    """
    retrieve all the goods link
    """
    page_num = 0
    list = []
    url = get_next_page_url(page_num)
    while url is not None:
        page_items_infos = []
        soup = bs.BeautifulSoup(get_page(url))
        pagelist = soup.findAll('div', {'id': 'plist'})
        for elem in pagelist:
            soup = bs.BeautifulSoup(str(elem))
            item_page_list = soup.findAll('div', {'class': 'p-name'})
            for item in item_page_list:
                soup = bs.BeautifulSoup(str(item))
                item_info = soup.find('a')
                list.append(item_info['href'])
                item_info_str = str(page_num * 60 + len(list)) + u'\t' + item_info.text + \
                                u'\t' + item_info['href'] + '\n'
                store_item_link_info(item_info_str.encode('utf-8'), FP_ITEM_INFO_LIST)
                # page_items_infos.append(item_info_str)
                print item_info_str

        # store_item_link_info(page_items_infos, FP_ITEM_INFO_LIST)
        page_num = page_num + 1
        url = get_next_page_url(page_num)
        print 'reading next page list...'
    return list

def analyze_file(filepath):
    content = restore_page(filepath)
    if content is not None:
        soup = bs.BeautifulSoup(content)
        detail_table = soup.find('table', {'class': 'Ptable'})
        soup = bs.BeautifulSoup(str(detail_table))
        item_para_name = soup.findAll('td', {'class': 'tdTitle'})
        for para_name in item_para_name:
            print para_name.text, ":", para_name.nextSibling.text

def analyze_content(url):
    """
    analyze the goods page
    """
    # soup = bs.BeautifulSoup(content)
    # item_detail_html = soup.findAll('ul', {'id': 'detail-list'})
    # item_detail = item_detail_html[0]
    # soup = bs.BeautifulSoup(str(item_detail))
    # detail = soup.find('ul')
    # print detail['class']
    pass

def store_goods_links(goods_links, path):
    """
    store the list of goods links into a file
    """
    pass

def test_analyze_content():
    # analyze_content('http://item.jd.com/1105329.html')
    analyze_file("test.html")
    pass

if __name__ == "__main__":
    if not check_file_exits(FP_ITEM_INFO_LIST):
        list = analyze_url_list()
        print "retrieved", len(list), "items"
    test_analyze_content()
    store_goods_links(list, "data/jd_lists.dat")
