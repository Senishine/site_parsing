"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""
import json
import requests
import os


def user_repos(username, token):
    response = requests.get('https://api.github.com/user/repos', auth=(username, token))
    data = response.json()
    with open('git_api.json', 'w') as file:
        json.dump(data, file, indent=4)
    for repo in data:
        print(repo['name'])


if __name__ == '__main__':
    token = os.environ.get("GITHUB_TOKEN")
    user_repos('Senishine', token)









