"""
1. Развернуть у себя на компьютере / виртуальной машине / хостинге MongoDB и реализовать функцию, которая будет
добавлять только новые вакансии / продукты в вашу базу.
"""
import json
from pymongo import MongoClient, InsertOne


def connect_to_db():
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies_db']  # указатель на БД
    python_vacancies = db.vacancy  # указатель на коллекцию
    return python_vacancies


def fill_db(file, collection):
    with open(file) as f:
        file_data = json.load(f)
        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)


def add_vacancy(collection, file):
    with open(file) as f:
        file_data = json.load(f)
        for item in file_data:
            if not collection.find_one(item):
                collection.insert_one(item)


if __name__ == '__main__':
    fill_db('python_vacancies.json', connect_to_db())
    add_vacancy(connect_to_db(), 'python_vacancies.json')
    #
    # data = connect_to_db().find({
    #     'vacancy_name': 'Data scientist'
    # })
    # for i in data:
    #     print(i)

    # all_data_1 = connect_to_db().find({})
    # for i in all_data_1:
    #     print(i)

    # connect_to_db().delete_many({})

    # all_data_1 = connect_to_db().find({})
    # count = 0
    # for i in all_data_1:
    #     count += 1
    # print(count)
