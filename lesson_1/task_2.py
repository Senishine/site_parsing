"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
пройдя авторизацию. Ответ сервера записать в файл.
"""

import json
import requests
import local_variables as variables


def get_vk(user, acc_token):
    response = requests.get(f'https://api.vk.com/method/groups.get?user_ids={user}& \
                fields=activity&extended=1&access_token={acc_token}&v=5.131')

    data = response.json()
    groups_lst = []
    for group in data["response"]["items"]:
        groups_lst.append(group['screen_name'])
    with open('user_groups.json', 'w', encoding='utf-8') as file:
        json.dump(groups_lst, file)


if __name__ == '__main__':
    get_vk(variables.user, variables.token)
