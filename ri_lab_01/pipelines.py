# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from datetime import datetime

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem

class RiLab01Pipeline(object):
    def process_item(self, item, spider):
        '''
        Processamento da string de data, para deixar de acordo com o que a tabela pede
        '''
        day, month, year, hour = item['date'].replace('de','').replace('às','').split()
        month = self.convert_month(month)
        hh, mm = hour.split(':')

        item['date'] = datetime(int(year), month, int(day), int(hh), int(mm), 00)        

        return item

    def convert_month(self, month):
        if month.lower() == 'janeiro':
            return 1
        elif month.lower() == 'fevereiro':
            return 2
        elif month.lower() == 'março':
            return 3
        elif month.lower() == 'abril':
            return 4
        elif month.lower() == 'maio':
            return 5
        elif month.lower() == 'junho':
            return 6
        elif month.lower() == 'julho':
            return 7
        elif month.lower() == 'agosto':
            return 8
        elif month.lower() == 'setembro':
            return 9
        elif month.lower() == 'outubro':
            return 10
        elif month.lower() == 'novembro':
            return 11
        elif month.lower() == 'dezembro':
            return 12
