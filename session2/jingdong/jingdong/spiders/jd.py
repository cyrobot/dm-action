# -*- coding: utf-8 -*-
import scrapy
import BeautifulSoup as bs
from scrapy import Request
import requests
import simplejson
import sys
sys.path.append('..')
import jingdong
from jingdong.items import JingdongItem
from jingdong.util import *

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = (
        'http://list.jd.com/list.html?cat=1320%2C1583%2C1590&page=',  # 食品
    )
    abandond = 0
    products = 0

    def parse(self, response):
        html = bs.BeautifulSoup(response._get_body())

        preq = []

        # 获取商品的地址
        plist = html.find('div', {'id': 'plist'})
        plist = plist.findAll('div', {'class': 'p-name'})
        for p in plist:
            href = p.find('a')['href']
            r = Request(href, callback=self.parse_product)
            preq.append(r)
        return preq

        # 获取下一页地址
        # try:
        #     next_list = html.find('div', {'class': 'pagin fr'})
        #     next_list = next_list.findAll('a')
        #     url = 'http://list.jd.com/list.html'
        #     for next_page in next_list:
        #         href = next_page['href']
        #         if href:
        #             href = url + href
        #             r = Request(href, callback=self.parse)
        #             preq.append(r)
        # except Exception, e:
        #     print e.message

    def parse_product(self, response):
        "获取商品详细信息"
        html = bs.BeautifulSoup(response._get_body())
        detail_list1 = html.find('div', {'id': 'product-detail-1'})
        detail_list2 = html.find('div', {'id': 'product-detail-2'})

        pdetail = {}
        pid = response._get_url().split('/')[-1].split('.')[0]
        self.products += 1
        #detail-1
        try:
            detail_list1 = detail_list1.find('ul', {'class': 'detail-list'})
            all_detail1 = detail_list1.findAll('li')
            for detail in all_detail1:
                detail_text = detail.text.replace(u'：', ':')
                key_val = unicode.split(detail_text, u':', 1)
                if len(key_val) == 2:
                    dict_append(pdetail, key_val[0], key_val[1])
                else:
                    # 说明字符编码不对，丢弃该数据
                    self.abandond += 1
                    print pid, '网页编码无法识别解析，丢弃{}/{}'.format(self.abandond, self.products)
                    return
        except Exception, e:
            print 'detail-1 exception:', e.message

        #detail-2
        try:
            all_detail2 = detail_list2.findAll('td', {'class': 'tdTitle'})
            if all_detail2:
                for detail in all_detail2:
                    dict_append(pdetail, key_val[0], key_val[1])
            else:
                all_detail2 = detail_list2.find('div', {'class': 'item-detail'})
                if all_detail2:
                    all_detail2 = all_detail2.findAll('p')
                    for detail in all_detail2:
                        detail_text = detail.text.replace(u'：', ':')
                        key_val = unicode.split(detail_text, u':', 1)
                        if len(key_val) == 2:
                            dict_append(pdetail, key_val[0], key_val[1])
        except Exception, e:
            print 'detail-2 exception:', e.message

        if len(pdetail) > 0:
            item = JingdongItem()
            item['id'] = pid
            item['detail'] = pdetail

            print 'product id', pid
            dict_print(pdetail)
            return self.parse_comment(response, item)
        return None

    def parse_comment(self, response, item):
        pid = response._get_url().split('/')[-1].split('.')[0]

        user_agent = {'GET': '', 'Host': "club.jd.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; rv:29.0) Gecko/20100101 Firefox/29.0",
            'Referer': 'http://item.jd.com/{}.html'.format(pid)}
        url = 'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(pid, 0)
        r = requests.get(url, headers=user_agent)
        if r:
            maxpagenum = r.json()['productCommentSummary']['commentCount'] // 10
        else:
            maxpagenum = 0

        print 'pid:', pid, 'comment page count:', maxpagenum
        reqs = []
        for i in xrange(maxpagenum + 1):
            url = 'http://club.jd.com/productpage/p-{}-s-0-t-3-p-{}.html'.format(pid, i)
            req = Request(url, callback=self.parse_comment_json)
            req.meta['item'] = item
            reqs.append(req)
        return reqs

    def parse_comment_json(self, response):
        pid = str.split(response._get_url(), '-')[1]
        print 'id:', pid

        content = response._get_body()
        try:
            comments = simplejson.loads(content, encoding='GBK')
            comments = [x['content'] for x in comments['comments']]
            item = response.meta['item']
            item['comment'] = comments
            print pid, 'comments:'
            list_print(comments)
        except Exception, e:
            print e.message
        return item
