#-*-coding: utf-8 -*-
__author__ = 'robert'

import urllib2
import BeautifulSoup as bs
import time

JD_FOOD_LINK_PREFIX = u"http://list.jd.com/list.html?cat=1320%2C1583%2C1590&page="
JD_FOOD_LINK_POSTFIX = u"&JL=6_0_0"

FP_ITEM_INFO_LIST = u'data/items_info.txt'

def get_page(urlstr):
    """
    get page content
    """
    content = urllib2.urlopen(urlstr).read();
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

def analyze_content(url):
    """
    analyze the goods page
    """
    soup = bs.BeautifulSoup(get_page(url))
    item_detail = soup.findAll('div', {'id': 'product-detail-2'})[0]
    soup = bs.BeautifulSoup(item_detail).find('table')
    print soup[0]

def store_goods_links(goods_links, path):
    """
    store the list of goods links into a file
    """
    pass

def test_analyze_content():
    analyze_content('http://item.jd.com/1237619734.html')

if __name__ == "__main__":
    # list = analyze_url_list()
    # print "retrieved", len(list), "items"
    test_analyze_content()
    store_goods_links(list, "data/jd_lists.dat")
