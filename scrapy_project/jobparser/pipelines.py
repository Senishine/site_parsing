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
        if spider.name == 'hhru':
            self.handle_hhru_salary(item)
        else:
            self.handle_superjob_salary(item)
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    @staticmethod
    def handle_hhru_salary(self, item):
        if item['salary_lst_items'][0] == 'от':
            item['salary_min'] = int(item['salary_lst_items'][1])
        if len(item['salary_lst_items']) == 4:
            item['salary_currency'] = item['salary_list'][3]
        if len(item['salary_lst_items']) >= 6:
            item['salary_currency'] = item['salary_list'][5]
        if item['salary_lst_items'][0] == 'до':
            item['salary_max'] = int(item['salary_lst_items'][1])
        if item['salary_lst_items'][2] == 'до':
            item['salary_max'] = int(item['salary_lst_items'][3])
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
            item['salary_tax'] = None
        return item

    @staticmethod
    def handle_superjob_salary(self, item):
        if len(item['salary_lst_items']) < 6:
            if 'от' in item['salary_lst_items'][0]:
                item['salary_min'] = int(item['salary_lst_items'][2][:-3])
                item['salary_currency'] = item['salary_lst_items'][2][-3:]
            if 'до' in item['salary_lst_items'][0]:
                item['salary_max'] = int(item['salary_lst_items'][2][:-3])
                item['salary_currency'] = item['salary_lst_items'][2][-3:]
        if len(item['salary_lst_items']) > 6:
            item['salary_min'] = int(item['salary_lst_items'][0])
            item['salary_max'] = int(item['salary_lst_items'][4])
            item['salary_currency'] = item['salary_lst_items'][6]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
        return item


