"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1.Наименование вакансии.
2.Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3.Ссылку на саму вакансию.
4.Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть одинаковая
для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""
import json
import requests
from bs4 import BeautifulSoup


def get_vacancies(url, page_count):
    result = []

    for i in range(page_count):
        response = requests.get(url, headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})

        for vacancy in vacancies:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).text
            tag = vacancy.find('a', {'class': 'bloko-link'})
            vacancy_link = tag['href']
            company = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).text
            source_site = base_url

            vacancy_data['vacancy_name'] = vacancy_name
            vacancy_data['min_salary'] = None
            vacancy_data['max_salary'] = None
            vacancy_data['currency'] = None
            vacancy_data['link'] = vacancy_link
            vacancy_data['website'] = source_site
            if vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                salary = salary.split()
                if salary[0] == 'от':  # ['от', '200', '000', 'rub']
                    vacancy_data['min_salary'] = int(f'{salary[1]}{salary[2]}')
                    vacancy_data['currency'] = salary[3]
                elif salary[0] == 'до':
                    vacancy_data['max_salary'] = int(f'{salary[1]}{salary[2]}')
                    vacancy_data['currency'] = salary[3]
                else:
                    vacancy_data['min_salary'] = int(f'{salary[0]}{salary[1]}')
                    vacancy_data['max_salary'] = int(f'{salary[3]}{salary[4]}')
                    vacancy_data['currency'] = salary[5]
            result.append(vacancy_data)
    return result


if __name__ == '__main__':
    pages_count = int(input('Enter the number of pages to view: '))

    base_url = 'https://spb.hh.ru'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/98.0.4758.82 Safari/537.36'}
    params = {'text': 'python', 'area': 1, 'currency_code': 'RUR', 'experience': 'doesNotMatter',
              'order_by': 'relevance',
              'search_period': 0, 'items_on_page': 20, 'no_magic': 'true', 'L_save_area': 'true'}

    hh_url = f'{base_url}/search/vacancy'
    res = get_vacancies(hh_url, pages_count)
    # print(len(res))
    with open(f'python_vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)


