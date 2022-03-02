"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска
продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос
проверяет оба поля)
"""
from pymongo import MongoClient


def get_vacancies(collection, salary):
    for vac in collection.find({'$or': [{'min_salary': {'$gt': salary}}, {'max_salary': {'$gt': salary}}]}):
        print(vac)


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    db = client['vacancies_db']  # указатель на БД
    python_vacancies = db.vacancy  # указатель на коллекцию
    get_vacancies(python_vacancies, 120000)
