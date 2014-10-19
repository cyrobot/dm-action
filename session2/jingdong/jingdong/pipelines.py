# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import simplejson
from util import *


class JingdongPipeline(object):

    def __init__(self):
        self.food_file = open('food.txt', 'wa')

    def process_item(self, item, spider):
        self.store_food(item)
        self.store_comment(item)
        return item

    def store_food(self, item):
        """
        存储至相应文件中
        2个文件，其中一个文件按照如下格式来存储
        1. 存储至一个文件中'food.txt' id,属性1:值1,属性2:值2,，...\n
        2. 以id为文件名，存储每条评论
        """
        food_property = item['id'] + '\t'
        detail = item['detail']
        for k in detail:
            food_property += k.encode('utf-8') + ':' + detail[k].encode('utf-8') + '\t'
        food_property = food_property[:-2]
        food_property += '\n'
        self.food_file.write(food_property)

    def store_comment(self, item):
        pass
