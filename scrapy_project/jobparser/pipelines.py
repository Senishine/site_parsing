import logging

import pyasn1_modules.rfc7906
from pymongo import MongoClient

#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.python_vacancies_scrapy

    def process_item(self, item, spider):
        try:
            if spider.name == 'hhru':
                self.handle_hhru_salary(item)
            else:
                self.handle_superjob_salary(item)
            print(f"item: {item}")
            collection = self.mongobase[spider.name]
            collection.insert_one(item)
        except Exception as e:
            logging.info('Error during processing item [item=%s, error=%s]', item, e)
        return item


    def handle_hhru_salary(self, item):
        elems = []
        for i in item['salary_lst_items']:
            elems.append(i.strip().replace('\xa0', ''))
        item['salary_lst_items'] = elems
        if 4 < len(elems) < 7 and 'от' in elems[0]:
            item['salary_min'] = int(''.join(elems[1].split()))
            item['salary_currency'] = elems[3]
            item['salary_max'] = None
        if 4 < len(elems) < 7 and 'до' in elems[0]:
            item['salary_max'] = int(''.join(elems[1].split()))
            item['salary_currency'] = elems[3]
            item['salary_min'] = None

        if len(elems) >= 7:
            item['salary_currency'] = elems[5]
            item['salary_min'] = int(''.join(elems[1].split()))
            item['salary_max'] = int(''.join(elems[3].split()))
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
        return item


    def handle_superjob_salary(self, item):
        for i in range(len(item['salary_lst_items'])):
            item['salary_lst_items'][i] = item['salary_lst_items'][i].replace(u'\xa0', u'')
        if len(item['salary_lst_items']) == 5:
            if 'от' in item['salary_lst_items'][0]:
                item['salary_min'] = int(item['salary_lst_items'][2][:-4])
                item['salary_currency'] = item['salary_lst_items'][2][-4:]
            if 'до' in item['salary_lst_items'][0]:
                item['salary_max'] = int(item['salary_lst_items'][2][:-4])
                item['salary_currency'] = item['salary_lst_items'][2][-4:]
        if len(item['salary_lst_items']) == 8:
            item['salary_min'] = int(item['salary_lst_items'][0])
            item['salary_max'] = int(item['salary_lst_items'][4])
            item['salary_currency'] = item['salary_lst_items'][6]
        if item['salary_lst_items'] == 'По договорённости':
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
        return item


