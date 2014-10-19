#-*-coding: utf-8 -*-
__author__ = 'robert'

import urllib2
import urllib
import os
import BeautifulSoup as bs
import time
import numpy.random as random
import requests

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
        analyze_content(content)

def analyze_comment_page(good_id):
    """
    analyze the review comments
    """
    page_no = 1
    retry_count = 0
    while True:
        comment_url = get_comment_page_url(good_id, page_no)
        print 'comment url:', comment_url
        comment_content = get_page(comment_url)
        if comment_content is None:
            retry_count += 1
            if retry_count > 3:
               break
            continue
        soup = bs.BeautifulSoup(comment_content)
        is_last = is_last_page(soup)
        tag_comments = soup.findAll('div', {'class': 'comment-content'})
        for tag_comment in tag_comments:
            soup = bs.BeautifulSoup(unicode(tag_comment))
            comment_heads = soup.findAll('dt')
            for comment_head in comment_heads:
                head_text = unicode.replace(comment_head.text, u'　', '')
                if head_text == u'心得：':
                    soup = bs.BeautifulSoup(unicode(comment_head.parent))
                    comment = soup.find('dd')
                    print comment.text
        if is_last:
            print 'good', good_id, 'is reviewed'
            break
        page_no += 1
        retry_count = 0
        time.sleep(random.randint(3, 7))

def is_last_page(soup):
    tag_page =  soup.find('div', {'class': 'pagin fr'})
    soup_page = bs.BeautifulSoup(str(tag_page))
    tag_next_page = soup_page.find('a', {'class': 'next'})
    if tag_next_page is None:
        return True
    return False

def abstracted_comments_js(soup):
    tag_js = soup.find('')

def get_comment_page_url(good_id, page_no):
    """
    http://club.jd.com/review/(good_id)-0-(page_no)-0.html
    """
    return 'http://club.jd.com/review/' + good_id + '-0-' + str(page_no) + '-0.html'

def analyze_content(content):
    """
    analyze the goods page
    """
    soup = bs.BeautifulSoup(content)
    tag_detail_list = soup.find('ul', {'class': 'detail-list'})
    tag_detail_table = soup.find('table', {'class': 'Ptable'})
    # detail-1
    soup = bs.BeautifulSoup(str(tag_detail_list))
    item_para = soup.findAll('li')
    for para in item_para:
        newtext = para.text.replace(u'：', ':')
        para_name, para_value = unicode.split(newtext, u':', 1)
        print para_name, ":", para_value
    #detail-2
    soup = bs.BeautifulSoup(str(tag_detail_table))
    item_para_name = soup.findAll('td', {'class': 'tdTitle'})
    for para_name in item_para_name:
        print para_name.text, ":", para_name.nextSibling.text

def getrate_jd(pid, pagenum):
    '''该函数用来获取商品ID是pid的第pagenum页的评论列表'''
    headers1 = {'GET': '', 'Host': "club.jd.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; rv:29.0) Gecko/20100101 Firefox/29.0",
            'Referer': 'http://item.jd.com/{}.html'.format(pid)}
    r = requests.get(
    'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(pid, pagenum), headers=headers1)
    try:
        aa = r.json()
        ss = [x['content'] for x in aa['comments']]
        for s in ss:
            print s
    except:
        print r.content

def post(url, data):
    # req = urllib2.Request(url)
    # data = urllib.urlencode(data)
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    # response = opener.open(req, data)
    # return response.read()
    pid = '1105329'
    headers1 = {'GET': '',
            'Host': "club.jd.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; rv:31.0) Gecko/20100101 Firefox/31.0",
            'Referer': 'http://item.jd.com/{}.html'.format(pid)}
    r1 = requests.get(
        'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(pid, 0), headers=headers1)
    maxpagenum = r1.json()['productCommentSummary']['commentCount'] // 10
    print maxpagenum
    for i in range(maxpagenum + 1):
        getrate_jd(pid, i)

def store_goods_links(goods_links, path):
    """
    store the list of goods links into a file
    """
    pass

def test_analyze_content():
    content = get_page('http://item.jd.com/837625.html')
    analyze_content(content)
    # analyze_comment_page('837625')
    # analyze_file("test.html")

def test_post_url(urlstr):
    post(urlstr, {'callback': 'jsonp1412005262195', '_': '1412007087758'})

if __name__ == "__main__":
    if not check_file_exits(FP_ITEM_INFO_LIST):
        list = analyze_url_list()
        print "retrieved", len(list), "items"
    test_analyze_content()
    # store_goods_links(list, "data/jd_lists.dat")
    # callback=jsonp1412005262195&_=1412007087758'
    # test_post_url('http://club.jd.com/productpage/p-1105329-s-0-t-3-p-1.html')
