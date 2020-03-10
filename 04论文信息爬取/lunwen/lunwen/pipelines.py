# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymongo

class LunwenPipeline(object):
    def __init__(self):
        #连接mongodb数据库
        client = pymongo.MongoClient('mongodb://localhost:27017')
        #连接老陈数据库
        self.db = client['laochen']
        #获取lunwen集合
        self.col = self.db['lunwen']
        
    def process_item(self, item, spider):
        print('----item-------------')
        print("数据插入成功：{}".format(item['title']))
        #获取每一页的item内容,并插入数据库
        self.col.insert_one(dict(item))

